"""Branchement des dépendances réelles (Voyage, Qdrant, Anthropic) du runner d'éval RAG."""

from dataclasses import dataclass

import anthropic
from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.rag.evaluation.judge import AnthropicJudge
from src.rag.evaluation.models import Answer, RetrievedChunk
from src.rag.evaluation.runner import FetchDocChunks, Generate, Retrieve

TEMPERATURE = 0.0
SCROLL_LIMIT = 10_000


@dataclass
class Deps:
    """Dépendances I/O prêtes à injecter dans run_eval."""

    retrieve: Retrieve
    generate: Generate
    fetch_doc_chunks: FetchDocChunks
    judge: AnthropicJudge
    valid_doc_ids: set[str]
    model: str
    judge_model: str
    collection_variant: str


def collection_variant(payloads: list[dict]) -> str:
    """Variante d'ingestion unique de la collection ; erreur si absente ou mixte."""

    variants = {p.get("ingestion_variant") for p in payloads}
    if variants == {None} or None in variants:
        raise ValueError(
            "collection sans ingestion_variant : ré-ingérer avec "
            "`python -m src.rag.ingestion --recreate --variant ...`"
        )
    if len(variants) > 1:
        raise ValueError(
            f"collection mixte {sorted(str(v) for v in variants)} : ré-ingérer avec --recreate"
        )
    return str(variants.pop())


def check_variant(declared: str, actual: str) -> None:
    """Refuse un label --variant qui ne correspond pas à la collection ingérée."""

    if declared != actual:
        raise ValueError(f"--variant {declared} mais la collection est ingérée en '{actual}'")


def _to_dict(chunk: RetrievedChunk) -> dict:
    """Reconvertit un chunk au format dict attendu par generator.format_context."""

    data: dict = {"text": chunk.text, "source": chunk.source or f"{chunk.doc_id}.pdf"}
    # le contexte isolé n'a pas de score de similarité
    if chunk.score:
        data["score"] = chunk.score
    return data


def build_deps(judge_model: str | None = None) -> Deps:
    """Construit les dépendances réelles ; imports paresseux (Qdrant local verrouille le disque)."""

    from src.config import ANTHROPIC_API_KEY, MODEL
    from src.rag import generator, retriever

    def retrieve(question: str, k: int) -> list[RetrievedChunk]:
        """Top-k Qdrant converti en RetrievedChunk."""

        hits = retriever.retrieve(question, top_k=k)
        return [
            RetrievedChunk(
                doc_id=h["doc_id"],
                chunk_index=h["chunk_index"],
                score=h["score"],
                text=h["text"],
                source=h["source"],
            )
            for h in hits
        ]

    def generate(question: str, chunks: list[RetrievedChunk]) -> Answer:
        """Génération à temperature=0 à partir des chunks fournis."""

        text = generator.generate_from_chunks(
            question, [_to_dict(c) for c in chunks], temperature=TEMPERATURE
        )
        return Answer(text=text)

    def fetch_doc_chunks(doc_id: str) -> list[RetrievedChunk]:
        """Tous les chunks d'un document, dans l'ordre du document."""

        points, _ = retriever.qdrant_client.scroll(
            collection_name=retriever.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))]
            ),
            limit=SCROLL_LIMIT,
            with_payload=True,
        )
        chunks = []
        for point in points:
            payload = point.payload or {}
            chunks.append(
                RetrievedChunk(
                    doc_id=payload["doc_id"],
                    chunk_index=payload["chunk_index"],
                    score=0.0,
                    text=payload["text"],
                    source=payload["source"],
                )
            )
        return sorted(chunks, key=lambda c: c.chunk_index)

    points, _ = retriever.qdrant_client.scroll(
        collection_name=retriever.COLLECTION_NAME,
        limit=SCROLL_LIMIT,
        with_payload=["doc_id", "ingestion_variant"],
    )
    payloads = [p.payload for p in points if p.payload]
    valid_doc_ids = {p["doc_id"] for p in payloads if "doc_id" in p}
    # Guard - une collection sans doc_id rendrait toute l'éval invalide
    if not valid_doc_ids:
        raise ValueError("collection sans doc_id : ré-ingérer le corpus (src/rag/ingestion.py)")

    chosen_judge_model = judge_model or MODEL
    judge = AnthropicJudge(anthropic.Anthropic(api_key=ANTHROPIC_API_KEY), chosen_judge_model)
    return Deps(
        retrieve=retrieve,
        generate=generate,
        fetch_doc_chunks=fetch_doc_chunks,
        judge=judge,
        valid_doc_ids=valid_doc_ids,
        model=MODEL,
        judge_model=chosen_judge_model,
        collection_variant=collection_variant(payloads),
    )
