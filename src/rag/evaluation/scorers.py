"""Scorers par type de question : points obligatoires et points interdits."""

from src.rag.eval_schema import Point, RagQuestion
from src.rag.evaluation.models import Answer, ScoreResult
from src.rag.evaluation.numbers import forme_presente


def _point_present(point: Point, text: str) -> bool:
    """Indique si l'une des formes acceptables du point apparaît dans le texte."""

    return any(forme_presente(forme, text) for forme in point.formes)


def score(question: RagQuestion, answer: Answer) -> ScoreResult:
    """Note une réponse : tous les points obligatoires présents, aucun point interdit."""

    # Guard - un scorer sans point obligatoire accepterait toute réponse
    if not question.points_obligatoires:
        raise ValueError(f"{question.id} : points_obligatoires vide, question non scorable")
    if any(p.verif == "juge" for p in (*question.points_obligatoires, *question.points_interdits)):
        raise NotImplementedError("points jugés par LLM : pas encore branchés")

    details: dict[str, bool] = {}
    for point in question.points_obligatoires:
        details[point.id] = _point_present(point, answer.text)
    for point in question.points_interdits:
        details[point.id] = not _point_present(point, answer.text)
    return ScoreResult(passed=all(details.values()), needs_review=False, details=details)
