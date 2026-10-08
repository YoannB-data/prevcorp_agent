"""Affiche les chunks stockés dans Qdrant (lecture seule) ; ne pas lancer pendant Streamlit."""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient  # noqa: E402

from src.rag.ingestion import COLLECTION_NAME, QDRANT_PATH  # noqa: E402

SCROLL_LIMIT = 10_000


def main() -> int:
    """Liste les chunks (doc, index, variante, mots, texte brut) puis un récapitulatif."""

    parser = argparse.ArgumentParser(description="Dump des chunks Qdrant")
    parser.add_argument("--doc", nargs="*", metavar="DOC_ID", help="limiter à ces doc_id")
    parser.add_argument("--summary", action="store_true", help="récapitulatif seul, sans texte")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    client = QdrantClient(path=str(QDRANT_PATH))
    points, _ = client.scroll(collection_name=COLLECTION_NAME, limit=SCROLL_LIMIT)
    payloads = sorted(
        (p.payload for p in points if p.payload),
        key=lambda p: (p["doc_id"], p["chunk_index"]),
    )
    if args.doc:
        payloads = [p for p in payloads if p["doc_id"] in args.doc]
    if not args.summary:
        for p in payloads:
            words = len(p["text"].split())
            variant = p.get("ingestion_variant", "?")
            print(f"--- {p['doc_id']} #{p['chunk_index']} [{variant}] {words} mots")
            print(p["text"])
    print("\nChunks par document :")
    for doc_id, n in sorted(Counter(p["doc_id"] for p in payloads).items()):
        print(f"  {doc_id}: {n}")
    print(f"Total : {len(payloads)}")
    print(f"Variantes : {dict(Counter(p.get('ingestion_variant', '?') for p in payloads))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
