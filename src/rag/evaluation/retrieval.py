"""Succès du retrieval : documents attendus ET points obligatoires retrouvés dans leurs chunks."""

from src.rag.eval_schema import RagQuestion
from src.rag.evaluation.models import RetrievalCheck, RetrievedChunk
from src.rag.evaluation.numbers import forme_presente


def check_retrieval(question: RagQuestion, chunks: list[RetrievedChunk]) -> RetrievalCheck:
    """Vérifie que le top-k contient les sources attendues et le contenu des points obligatoires.

    Une forme ne compte que si elle figure dans un chunk d'un document de sources_attendues :
    le corpus partage volontairement des valeurs entre documents.
    """

    attendus = set(question.sources_attendues)
    docs_manquants = sorted(attendus - {c.doc_id for c in chunks})
    textes = [c.text for c in chunks if c.doc_id in attendus]
    # Les points interdits sont des formulations de mauvaise source : leur absence est normale
    points_absents = [
        p.id
        for p in question.points_obligatoires
        if not any(forme_presente(forme, texte) for forme in p.formes for texte in textes)
    ]
    return RetrievalCheck(
        ok=not docs_manquants and not points_absents,
        docs_manquants=docs_manquants,
        points_absents=points_absents,
    )
