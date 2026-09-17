"""
Composant de recherche RAG — question → chunks pertinents depuis Qdrant
"""

import os
from pathlib import Path

import voyageai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

load_dotenv()

QDRANT_PATH = Path(__file__).parent.parent.parent / "qdrant_storage"
COLLECTION_NAME = "prevcorp_docs"
EMBEDDING_MODEL = "voyage-multilingual-2"
TOP_K = 5

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
qdrant_client = QdrantClient(path=str(QDRANT_PATH))


def retrieve(
    question: str,
    top_k: int = TOP_K,
    doc_type: str | None = None,
) -> list[dict]:
    """
    Recherche les chunks les plus pertinents pour une question.

    Args:
        question: question en langage naturel
        top_k: nombre de chunks à retourner
        doc_type: filtre optionnel sur le type de document
                  (conditions_generales, fiche_parametrage, faq, note_technique, circulaire)

    Returns:
        Liste de dicts avec text, source, doc_type, score
    """
    result = voyage_client.embed([question], model=EMBEDDING_MODEL, input_type="query")
    query_vector = [float(x) for x in result.embeddings[0]]

    search_filter = None
    if doc_type:
        search_filter = Filter(
            must=[FieldCondition(key="doc_type", match=MatchValue(value=doc_type))]
        )

    hits = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        query_filter=search_filter,
        with_payload=True,
    ).points

    results = []
    for hit in hits:
        # Guard - with_payload=True garantit un payload non vide pour chaque hit
        assert hit.payload is not None
        results.append(
            {
                "text": hit.payload["text"],
                "source": hit.payload["source"],
                "doc_type": hit.payload["doc_type"],
                "chunk_index": hit.payload["chunk_index"],
                "score": round(hit.score, 4),
            }
        )
    return results


if __name__ == "__main__":
    question = "Quel est le délai de carence pour la garantie ITT ?"
    results = retrieve(question, top_k=3)
    for i, r in enumerate(results, 1):
        print(f"\n--- Chunk {i} | {r['source']} | score={r['score']}")
        print(r["text"][:300])
