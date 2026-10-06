"""Orchestration d'un run d'éval RAG : aucune logique de diagnostic ni de scoring ici."""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from src.rag.eval_schema import RagQuestion, load_questions
from src.rag.evaluation.diagnose import diagnose
from src.rag.evaluation.judge import Judge
from src.rag.evaluation.models import (
    Answer,
    Diagnostic,
    QuestionResult,
    Report,
    RetrievedChunk,
)
from src.rag.evaluation.report import hash_yaml
from src.rag.evaluation.retrieval import check_retrieval
from src.rag.evaluation.scorers import score

Retrieve = Callable[[str, int], list[RetrievedChunk]]
Generate = Callable[[str, list[RetrievedChunk]], Answer]
FetchDocChunks = Callable[[str], list[RetrievedChunk]]


def _contexte_isole(
    question: RagQuestion, fetch_doc_chunks: FetchDocChunks
) -> list[RetrievedChunk]:
    """Document entier de chaque doc_id de contexte_effectif, jamais issu du retrieval."""

    chunks: list[RetrievedChunk] = []
    for doc_id in question.contexte_effectif:
        doc_chunks = fetch_doc_chunks(doc_id)
        # Guard - un contexte isolé vide fausserait I en silence
        if not doc_chunks:
            raise ValueError(f"aucun chunk pour le doc_id {doc_id!r} (contexte isolé)")
        chunks.extend(doc_chunks)
    return chunks


def _run_question(
    question: RagQuestion,
    k: int,
    retrieve: Retrieve,
    generate: Generate,
    fetch_doc_chunks: FetchDocChunks,
    judge: Judge,
) -> QuestionResult:
    """Évalue une question seule : retrieval, run e2e, run isolé, diagnostic."""

    chunks = retrieve(question.question, k)
    answer_e2e = generate(question.question, chunks)
    answer_iso = generate(question.question, _contexte_isole(question, fetch_doc_chunks))
    e2e = score(question, answer_e2e, judge)
    isolated = score(question, answer_iso, judge)
    retrieval = None if question.type == "sans_reponse" else check_retrieval(question, chunks)
    diagnostic = diagnose(None if retrieval is None else retrieval.ok, e2e.passed, isolated.passed)
    return QuestionResult(
        id=question.id,
        type=question.type,
        retrieval=retrieval,
        e2e=e2e,
        isolated=isolated,
        diagnostic=diagnostic,
        chunks=chunks,
        answer_e2e=answer_e2e.text,
        answer_isolated=answer_iso.text,
    )


def run_eval(
    yaml_path: Path,
    k: int,
    ingestion_variant: str,
    *,
    retrieve: Retrieve,
    generate: Generate,
    fetch_doc_chunks: FetchDocChunks,
    judge: Judge,
    valid_doc_ids: set[str],
    model: str,
    judge_model: str,
    temperature: float = 0.0,
    ids: list[str] | None = None,
    now: datetime | None = None,
) -> Report:
    """Rejoue les questions du YAML et rassemble les résultats dans un rapport."""

    questions = load_questions(yaml_path, valid_doc_ids)
    non_scorables = [q.id for q in questions if not q.points_obligatoires]
    # Guard - échoue avant tout appel payant si des questions ne sont pas scorables
    if non_scorables:
        raise ValueError(f"points_obligatoires vide pour : {non_scorables}")
    if ids:
        questions = [q for q in questions if q.id in ids]

    report = Report(
        date=now or datetime.now(),
        yaml_hash=hash_yaml(yaml_path),
        model=model,
        judge_model=judge_model,
        temperature=temperature,
        k=k,
        ingestion_variant=ingestion_variant,
    )
    for question in questions:
        try:
            result = _run_question(question, k, retrieve, generate, fetch_doc_chunks, judge)
        except Exception as exc:
            # Catch-all - une erreur d'I/O sur une question ne doit pas perdre le run
            result = QuestionResult(
                id=question.id,
                type=question.type,
                retrieval=None,
                e2e=None,
                isolated=None,
                diagnostic=Diagnostic.ERREUR,
                error=f"{type(exc).__name__}: {exc}",
            )
        report.results.append(result)
    return report
