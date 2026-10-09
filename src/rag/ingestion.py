"""
Pipeline d'ingestion : PDF → texte → chunks → embeddings Voyage → Qdrant
"""

import argparse
import hashlib
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Literal

import voyageai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.rag.metadata import (
    build_context_prefix,
    doc_type_from_filename,
    extract_contract_info,
    extract_title,
)
from src.rag.pdf_text import extract_text

load_dotenv()

CORPUS_DIR = Path(__file__).parent.parent.parent / "corpus"
QDRANT_PATH = Path(__file__).parent.parent.parent / "qdrant_storage"
COLLECTION_NAME = "prevcorp_docs"
EMBEDDING_MODEL = "voyage-multilingual-2"
CHUNK_SIZE = 150
CHUNK_OVERLAP = 20
MAX_ARTICLE_WORDS = 300
# Lookahead : le titre de l'article reste en tête de sa section
ARTICLE_START = re.compile(r"(?m)^(?=Article \d+ — )")

Variant = Literal["none", "prefix", "prefix_article"]
PREFIXED_VARIANTS = ("prefix", "prefix_article")


def default_clients() -> tuple[voyageai.Client, QdrantClient]:
    """Ouvre Voyage et Qdrant local (verrou disque) ; appelé à l'exécution, pas à l'import."""

    return voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY")), QdrantClient(path=str(QDRANT_PATH))


# ─── Chunking ────────────────────────────────────────────────────────────────


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Découpe le texte en chunks avec overlap, en respectant les fins de phrase."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return [c for c in chunks if len(c.strip()) > 50]


def chunk_by_article(text: str, max_words: int = MAX_ARTICLE_WORDS) -> list[str]:
    """Une section par « Article N — » ; texte sans article : découpage à taille fixe."""

    sections = ARTICLE_START.split(text)
    # Guard - sans article (Résumés, FAQ), on garde le découpage historique
    if len(sections) == 1:
        return chunk_text(text)
    chunks: list[str] = []
    for section in sections:
        words = section.split()
        if not words:
            continue
        if len(words) <= max_words:
            chunks.append(" ".join(words))
            continue
        head, _, body = section.partition("\n")
        # Le préambule n'a pas de titre à répéter ; un article oui
        title = head.strip() if head.startswith("Article ") else ""
        pieces = chunk_text(body if title else section)
        chunks.extend(f"{title} {piece}".strip() for piece in pieces)
    return chunks


# ─── Métadonnées ─────────────────────────────────────────────────────────────


def chunk_id(pdf_path: Path, chunk_index: int) -> str:
    """Génère un ID déterministe pour chaque chunk."""
    raw = f"{pdf_path.name}_{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


# ─── Qdrant ──────────────────────────────────────────────────────────────────


def ensure_collection(qdrant: QdrantClient) -> None:
    """Crée la collection Qdrant si elle n'existe pas."""

    existing = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' créée.")
    else:
        print(f"Collection '{COLLECTION_NAME}' existante — on continue.")


def upsert_chunks(
    qdrant: QdrantClient,
    chunks: list[str],
    embeddings: list[list[float]],
    pdf_path: Path,
    variant: Variant,
) -> None:
    """Insère les chunks bruts + embeddings + métadonnées dans Qdrant."""

    doc_type = doc_type_from_filename(pdf_path.name)
    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=chunk_id(pdf_path, i),  # ID déterministe (idempotent)
                vector=vector,
                payload={
                    "text": chunk,
                    "source": pdf_path.name,
                    "doc_id": pdf_path.stem,
                    "doc_type": doc_type,
                    "chunk_index": i,
                    # Lu par l'éval pour refuser un label qui ne correspond pas à l'index
                    "ingestion_variant": variant,
                },
            )
        )
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)


# ─── Préfixe de contexte ─────────────────────────────────────────────────────


def embedding_text(chunk: str, prefix: str) -> str:
    """Texte envoyé à l'embedding : préfixe, saut de ligne, chunk brut."""

    return f"{prefix}\n{chunk}"


def document_prefix(text: str, pdf_path: Path) -> str:
    """Préfixe de contexte d'un document ; lève PrefixConstructionError plutôt que de dégrader."""

    doc_type = doc_type_from_filename(pdf_path.name)
    if doc_type == "resume_contrat":
        contract = extract_contract_info(text, pdf_path.name)
        return build_context_prefix("", doc_type, contract)
    return build_context_prefix(extract_title(text, pdf_path.name), doc_type, None)


# ─── Pipeline principal ───────────────────────────────────────────────────────


def ingest_pdf(
    pdf_path: Path,
    voyage: voyageai.Client,
    qdrant: QdrantClient,
    variant: Variant = "none",
) -> tuple[int, int]:
    """Ingère un seul PDF. Retourne (chunks insérés, chunks dont l'embedding est préfixé)."""

    text = extract_text(pdf_path)
    if not text.strip():
        print(f"  ⚠ Texte vide : {pdf_path.name}")
        return 0, 0
    chunks = chunk_by_article(text) if variant == "prefix_article" else chunk_text(text)
    if variant in PREFIXED_VARIANTS:
        prefix = document_prefix(text, pdf_path)
        embedded = [embedding_text(c, prefix) for c in chunks]
    else:
        embedded = chunks
    result = voyage.embed(embedded, model=EMBEDDING_MODEL, input_type="document")
    embeddings = [[float(x) for x in vector] for vector in result.embeddings]
    upsert_chunks(qdrant, chunks, embeddings, pdf_path, variant)
    return len(chunks), len(chunks) if variant in PREFIXED_VARIANTS else 0


def ingest_corpus(
    corpus_dir: Path = CORPUS_DIR,
    variant: Variant = "none",
    clients: tuple[voyageai.Client, QdrantClient] | None = None,
) -> int:
    """Ingère tous les PDFs du corpus et affiche les chunks préfixés par type. Retourne le total."""

    voyage, qdrant = clients or default_clients()
    ensure_collection(qdrant)
    pdfs = sorted(corpus_dir.glob("*.pdf"))
    if not pdfs:
        print(f"Aucun PDF trouvé dans {corpus_dir}")
        return 0
    print(f"\n{len(pdfs)} PDFs à ingérer (variante : {variant})...\n")
    per_type: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for pdf_path in pdfs:
        n, n_prefixed = ingest_pdf(pdf_path, voyage, qdrant, variant)
        stats = per_type[doc_type_from_filename(pdf_path.name)]
        stats[0] += n
        stats[1] += n_prefixed
        print(f"  ✓ {pdf_path.name} — {n} chunks")
    print("\nChunks préfixés / chunks, par type de document :")
    for doc_type, (n, n_prefixed) in sorted(per_type.items()):
        print(f"  {doc_type}: {n_prefixed}/{n}")
    total = sum(n for n, _ in per_type.values())
    print(f"\n✅ Ingestion terminée : {total} chunks dans Qdrant")
    return total


def recreate_collection(qdrant: QdrantClient) -> None:
    """Supprime la collection si elle existe, pour repartir d'un index vide."""

    if COLLECTION_NAME in [c.name for c in qdrant.get_collections().collections]:
        qdrant.delete_collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' supprimée.")


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI : --variant choisit l'embedding, --recreate vide l'index avant."""

    parser = argparse.ArgumentParser(description="Ingestion du corpus PrevCorp dans Qdrant")
    parser.add_argument("--variant", choices=["none", "prefix", "prefix_article"], default="none")
    parser.add_argument("--recreate", action="store_true", help="supprime la collection avant")
    args = parser.parse_args(argv)
    clients = default_clients()
    if args.recreate:
        recreate_collection(clients[1])
    ingest_corpus(variant=args.variant, clients=clients)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
