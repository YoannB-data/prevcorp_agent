"""Scorers par type de question : points obligatoires et points interdits."""

from src.rag.eval_schema import Point, RagQuestion
from src.rag.evaluation.judge import Judge
from src.rag.evaluation.models import Answer, ScoreResult
from src.rag.evaluation.numbers import forme_presente


def _point_present(point: Point, text: str) -> bool:
    """Indique si l'une des formes acceptables du point apparaît dans le texte."""

    return any(forme_presente(forme, text) for forme in point.formes)


def score(question: RagQuestion, answer: Answer, judge: Judge | None = None) -> ScoreResult:
    """Note une réponse : tous les points obligatoires affirmés, aucun point interdit.

    Les points `deterministe` sont notés par extraction ; les points `juge` passent par le juge
    (un seul appel) et marquent le résultat « à vérifier à la main ».
    """

    # Guard - un scorer sans point obligatoire accepterait toute réponse
    if not question.points_obligatoires:
        raise ValueError(f"{question.id} : points_obligatoires vide, question non scorable")

    obligatoires = question.points_obligatoires
    interdits = question.points_interdits
    a_juger = [p for p in (*obligatoires, *interdits) if p.verif == "juge"]
    # Guard - un point jugé sans juge ne peut pas être noté silencieusement
    if a_juger and judge is None:
        raise ValueError(f"{question.id} : points verif=juge sans juge fourni")
    verdicts = judge.evaluate(question, answer.text, a_juger) if judge and a_juger else {}

    def affirme(point: Point) -> bool:
        """Verdict « la réponse affirme ce point », par juge ou par extraction."""

        if point.verif == "juge":
            return verdicts[point.id]
        return _point_present(point, answer.text)

    details = {p.id: affirme(p) for p in obligatoires}
    details.update({p.id: not affirme(p) for p in interdits})
    return ScoreResult(passed=all(details.values()), needs_review=bool(a_juger), details=details)
