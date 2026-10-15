"""Diagnostic retrieval seul (K=20) sur les questions de croisement en échec."""

from pathlib import Path

from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.rag.evaluation.models import RetrievedChunk
from src.rag.evaluation.retrieval import check_retrieval
from src.rag.evaluation.schema import RagQuestion, load_questions
from src.rag.retriever import COLLECTION_NAME, qdrant_client, retrieve

EVAL_SET_PATH = Path("evals/rag/eval_set.yml")
K = 20
QUESTION_IDS = ["RC03", "RC20", "RC22", "RC24", "RC25"]


def target_questions(valid_doc_ids: set[str]) -> list[RagQuestion]:
    """Questions ciblées de l'eval set, validées par le schéma du runner."""

    return [q for q in load_questions(EVAL_SET_PATH, valid_doc_ids) if q.id in QUESTION_IDS]


def indexed_doc_ids() -> dict[str, int]:
    """Compte les chunks par doc_id sur toute la collection."""

    counts: dict[str, int] = {}
    offset = None
    while True:
        points, offset = qdrant_client.scroll(
            COLLECTION_NAME, limit=256, offset=offset, with_payload=["doc_id"]
        )
        for p in points:
            doc_id = (p.payload or {}).get("doc_id")
            counts[doc_id] = counts.get(doc_id, 0) + 1
        if offset is None:
            return counts


def main() -> None:
    """Affiche rang des sources attendues, top-5 réel et chunks indexés."""

    counts = indexed_doc_ids()
    questions = target_questions(set(counts))
    all_expected: set[str] = set()
    print(f"\n=== Retrieval seul, K={K} ===\n")
    for q in questions:
        expected = q.sources_attendues
        all_expected.update(expected)
        hits = retrieve(q.question, top_k=K)
        ranks: dict[str, int | None] = {src: None for src in expected}
        for rank, hit in enumerate(hits, start=1):
            if hit["doc_id"] in ranks and ranks[hit["doc_id"]] is None:
                ranks[hit["doc_id"]] = rank
        chunks = [
            RetrievedChunk(h["doc_id"], h["chunk_index"], h["score"], h["text"], h["source"])
            for h in hits
        ]
        print(f"{q.id}  R = {check_retrieval(q, chunks)}")
        for src, rank in ranks.items():
            verdict = "ABSENT" if rank is None else f"rang {rank}"
            print(f"  {src:<40} {verdict}")
        print(f"  top-5 réel : {[h['doc_id'] for h in hits[:5]]}\n")

    print("=== Chunks indexés par source attendue ===\n")
    for src in sorted(all_expected):
        n = qdrant_client.count(
            COLLECTION_NAME,
            count_filter=Filter(must=[FieldCondition(key="doc_id", match=MatchValue(value=src))]),
            exact=True,
        ).count
        print(f"  {src:<40} {n} chunks")
        if n == 0:
            print(f"  -> ABSENT de la collection ; doc_id présents : {sorted(map(str, counts))}")


if __name__ == "__main__":
    main()
