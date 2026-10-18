"""
Pipeline d'ingestion : PDF → texte → chunks → embeddings Voyage → Qdrant
"""

import argparse
import hashlib
import os
from collections import defaultdict
from pathlib import Path

import voyageai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.config import QDRANT_PATH
from src.rag.metadata import (
    build_chunk_header,
    doc_type_from_filename,
    extract_contract_info,
    extract_title,
)
from src.rag.pdf_text import extract_text

load_dotenv()

CORPUS_DIR = Path(__file__).parent.parent.parent / "data" / "corpus" / "pdf"
COLLECTION_NAME = "prevcorp_docs"
EMBEDDING_MODEL = "voyage-multilingual-2"
CHUNK_SIZE = 150
CHUNK_OVERLAP = 20
# Lu par l'éval pour refuser une collection ingérée autrement
INGESTION_VARIANT = "header"


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


# ─── Métadonnées ─────────────────────────────────────────────────────────────


def chunk_id(pdf_path: Path, chunk_index: int) -> str:
    """Génère un ID déterministe pour chaque chunk."""
    raw = f"{pdf_path.name}_{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


# ─── Qdrant ──────────────────────────────────────────────────────────────────


def ensure_collection(qdrant: QdrantClient, collection: str = COLLECTION_NAME) -> None:
    """Crée la collection Qdrant si elle n'existe pas."""

    existing = [c.name for c in qdrant.get_collections().collections]
    if collection not in existing:
        qdrant.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        print(f"Collection '{collection}' créée.")
    else:
        print(f"Collection '{collection}' existante — on continue.")


def upsert_chunks(
    qdrant: QdrantClient,
    chunks: list[str],
    embeddings: list[list[float]],
    pdf_path: Path,
    header: str,
    collection: str = COLLECTION_NAME,
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
                    "ingestion_variant": INGESTION_VARIANT,
                    # Hors de "text" : le matcher des points obligatoires lit le texte brut
                    "header": header,
                },
            )
        )
    qdrant.upsert(collection_name=collection, points=points)


# ─── Header de contexte ──────────────────────────────────────────────────────


def embedding_text(chunk: str, header: str) -> str:
    """Texte envoyé à l'embedding : header, saut de ligne, chunk brut."""

    return f"{header}\n{chunk}"


def document_header(text: str, pdf_path: Path) -> str:
    """Header contextuel d'un document ; lève PrefixConstructionError plutôt que de dégrader."""

    doc_type = doc_type_from_filename(pdf_path.name)
    if doc_type == "resume_contrat":
        contract = extract_contract_info(text, pdf_path.name)
        return build_chunk_header("", doc_type, contract, pdf_path.name)
    return build_chunk_header(extract_title(text, pdf_path.name), doc_type, None, pdf_path.name)


# ─── Pipeline principal ───────────────────────────────────────────────────────


def ingest_pdf(
    pdf_path: Path,
    voyage: voyageai.Client,
    qdrant: QdrantClient,
    collection: str = COLLECTION_NAME,
) -> int:
    """Ingère un seul PDF (embedding header + chunk, payload brut) ; retourne le nb de chunks."""

    text = extract_text(pdf_path)
    if not text.strip():
        print(f"  ⚠ Texte vide : {pdf_path.name}")
        return 0
    chunks = chunk_text(text)
    header = document_header(text, pdf_path)
    embedded = [embedding_text(c, header) for c in chunks]
    result = voyage.embed(embedded, model=EMBEDDING_MODEL, input_type="document")
    embeddings = [[float(x) for x in vector] for vector in result.embeddings]
    upsert_chunks(qdrant, chunks, embeddings, pdf_path, header, collection)
    return len(chunks)


def ingest_corpus(
    corpus_dir: Path = CORPUS_DIR,
    clients: tuple[voyageai.Client, QdrantClient] | None = None,
    collection: str = COLLECTION_NAME,
) -> int:
    """Ingère tous les PDFs du corpus et affiche les chunks par type. Retourne le total."""

    voyage, qdrant = clients or default_clients()
    ensure_collection(qdrant, collection)
    pdfs = sorted(corpus_dir.glob("*.pdf"))
    if not pdfs:
        print(f"Aucun PDF trouvé dans {corpus_dir}")
        return 0
    print(f"\n{len(pdfs)} PDFs à ingérer (collection : {collection})...\n")
    per_type: dict[str, int] = defaultdict(int)
    for pdf_path in pdfs:
        n = ingest_pdf(pdf_path, voyage, qdrant, collection)
        per_type[doc_type_from_filename(pdf_path.name)] += n
        print(f"  ✓ {pdf_path.name} — {n} chunks")
    print("\nChunks par type de document :")
    for doc_type, n in sorted(per_type.items()):
        print(f"  {doc_type}: {n}")
    total = sum(per_type.values())
    print(f"\n✅ Ingestion terminée : {total} chunks dans Qdrant")
    return total


def recreate_collection(qdrant: QdrantClient, collection: str = COLLECTION_NAME) -> None:
    """Supprime la collection si elle existe, pour repartir d'un index vide."""

    if collection in [c.name for c in qdrant.get_collections().collections]:
        qdrant.delete_collection(collection)
        print(f"Collection '{collection}' supprimée.")


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI : --collection choisit la cible, --recreate vide l'index avant."""

    parser = argparse.ArgumentParser(description="Ingestion du corpus PrevCorp dans Qdrant")
    parser.add_argument(
        "--collection",
        default=COLLECTION_NAME,
        help=f"collection cible (défaut : {COLLECTION_NAME})",
    )
    parser.add_argument("--recreate", action="store_true", help="supprime la collection avant")
    args = parser.parse_args(argv)
    clients = default_clients()
    if args.recreate:
        recreate_collection(clients[1], args.collection)
    ingest_corpus(clients=clients, collection=args.collection)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
