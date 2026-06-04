"""
Pipeline d'ingestion : PDF → texte → chunks → embeddings Voyage → Qdrant
"""

import hashlib
import os
from pathlib import Path

import pdfplumber
import voyageai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

CORPUS_DIR = Path(__file__).parent.parent.parent / "corpus"
QDRANT_PATH = Path(__file__).parent.parent.parent / "qdrant_storage"
COLLECTION_NAME = "prevcorp_docs"
EMBEDDING_MODEL = "voyage-multilingual-2"
CHUNK_SIZE = 150
CHUNK_OVERLAP = 20

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
qdrant_client = QdrantClient(path=str(QDRANT_PATH))


# ─── Extraction texte ────────────────────────────────────────────────────────


def extract_text(pdf_path: Path) -> str:
    """Extrait texte + tableaux d'un PDF, en traitant les tableaux séparément."""
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            blocks = []
            # Tableaux
            for table in page.extract_tables():
                if not table:
                    continue
                header = table[0]
                rows = table[1:]
                table_lines = [" | ".join(str(c) for c in header)]
                table_lines += [" | ".join(str(c) for c in row) for row in rows]
                blocks.append("\n".join(table_lines))
            # Texte hors tableaux
            text = page.extract_text()
            if text:
                blocks.append(text.strip())
            pages_text.append("\n\n".join(blocks))
    return "\n\n".join(pages_text)


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


def doc_type_from_filename(filename: str) -> str:
    """Infère le type de document depuis le nom de fichier."""
    name = filename.upper()
    if name.startswith("CG_"):
        return "conditions_generales"
    if name.startswith("FICHE_"):
        return "fiche_parametrage"
    if name.startswith("FAQ_"):
        return "faq"
    if name.startswith("NT_"):
        return "note_technique"
    if name.startswith("CIRC_"):
        return "circulaire"
    return "autre"


def chunk_id(pdf_path: Path, chunk_index: int) -> str:
    """Génère un ID déterministe pour chaque chunk."""
    raw = f"{pdf_path.name}_{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


# ─── Qdrant ──────────────────────────────────────────────────────────────────


def ensure_collection() -> None:
    """Crée la collection Qdrant si elle n'existe pas."""
    existing = [c.name for c in qdrant_client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' créée.")
    else:
        print(f"Collection '{COLLECTION_NAME}' existante — on continue.")


def upsert_chunks(chunks: list[str], embeddings: list[list[float]], pdf_path: Path) -> None:
    """Insère les chunks + embeddings + métadonnées dans Qdrant."""
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
                    "doc_type": doc_type,
                    "chunk_index": i,
                },
            )
        )
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)


# ─── Pipeline principal ───────────────────────────────────────────────────────


def ingest_pdf(pdf_path: Path) -> int:
    """Ingère un seul PDF. Retourne le nombre de chunks insérés."""
    text = extract_text(pdf_path)
    if not text.strip():
        print(f"  ⚠ Texte vide : {pdf_path.name}")
        return 0
    chunks = chunk_text(text)
    result = voyage_client.embed(chunks, model=EMBEDDING_MODEL, input_type="document")
    upsert_chunks(chunks, result.embeddings, pdf_path)
    return len(chunks)


def ingest_corpus(corpus_dir: Path = CORPUS_DIR) -> None:
    """Ingère tous les PDFs du corpus."""
    ensure_collection()
    pdfs = sorted(corpus_dir.glob("*.pdf"))
    if not pdfs:
        print(f"Aucun PDF trouvé dans {corpus_dir}")
        return
    print(f"\n{len(pdfs)} PDFs à ingérer...\n")
    total_chunks = 0
    for pdf_path in pdfs:
        n = ingest_pdf(pdf_path)
        total_chunks += n
        print(f"  ✓ {pdf_path.name} — {n} chunks")
    print(f"\n✅ Ingestion terminée : {total_chunks} chunks dans Qdrant")


if __name__ == "__main__":
    ingest_corpus()
