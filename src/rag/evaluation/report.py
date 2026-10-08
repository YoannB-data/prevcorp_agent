"""Rapport markdown d'un run d'éval RAG : en-tête, synthèse, détail par question."""

import hashlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from src.rag.evaluation.models import QuestionResult, Report, ScoreResult

CONTEXTE_ISOLE = "document entier"
EXTRAIT_CHARS = 300
TYPES = ("fait_simple", "chiffre_precis", "croisement", "sans_reponse")


def hash_yaml(path: Path) -> str:
    """Empreinte courte (sha256, 12 caractères) du contenu exact du YAML."""

    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def report_filename(report: Report) -> str:
    """Nom de fichier : date + variante d'ingestion + hash du YAML."""

    stamp = report.date.strftime("%Y%m%d_%H%M%S")
    return f"rag_{stamp}_{report.ingestion_variant}_{report.yaml_hash}.md"


@dataclass(frozen=True)
class Tally:
    """Compte de réussites sur un dénominateur effectif."""

    passed: int = 0
    total: int = 0

    def __str__(self) -> str:
        """Affiche « réussites/dénominateur » ou N/A si le dénominateur est nul."""

        return f"{self.passed}/{self.total}" if self.total else "N/A"


def _tally(flags: list[bool]) -> Tally:
    """Compte les True d'une liste de verdicts."""

    return Tally(passed=sum(flags), total=len(flags))


def summarize(results: list[QuestionResult], type_: str | None = None) -> dict[str, Tally]:
    """Scores R/E/I sur les seules questions sans erreur d'I/O, par type si demandé."""

    kept = [r for r in results if r.error is None and (type_ is None or r.type == type_)]
    return {
        "R": _tally([r.retrieval.ok for r in kept if r.retrieval is not None]),
        "E": _tally([r.e2e.passed for r in kept if r.e2e is not None]),
        "I": _tally([r.isolated.passed for r in kept if r.isolated is not None]),
    }


def _verdict(score: ScoreResult | None) -> str:
    """Verdict lisible d'un score, avec la marque de relecture manuelle."""

    if score is None:
        return "—"
    mark = " ⚠ à vérifier à la main" if score.needs_review else ""
    return ("OK" if score.passed else "KO") + mark


def render_header(report: Report) -> str:
    """En-tête de reproductibilité : tout ce qui change le résultat d'un run."""

    return "\n".join(
        [
            "# Rapport d'éval RAG",
            "",
            f"- Date : {report.date.isoformat(timespec='seconds')}",
            f"- Hash du YAML : {report.yaml_hash}",
            f"- Modèle : {report.model}",
            f"- Modèle du juge : {report.judge_model}",
            f"- Temperature : {report.temperature}",
            f"- k : {report.k}",
            f"- Variante d'ingestion : {report.ingestion_variant} (vérifiée contre la collection)",
            f"- Contexte isolé : {CONTEXTE_ISOLE}",
            "",
        ]
    )


def render_summary(report: Report) -> str:
    """Synthèse : scores par type avec dénominateurs, erreurs d'I/O, répartition des diagnostics."""

    erreurs = [r for r in report.results if r.error is not None]
    lines = [
        "## Synthèse",
        "",
        f"Questions : {len(report.results)} dont {len(erreurs)} en erreur d'I/O "
        "(exclues des scores et des dénominateurs ci-dessous).",
        "",
        "| Type | R (retrieval) | E (end-to-end) | I (isolé) |",
        "|---|---|---|---|",
    ]
    for label, type_ in [("**Tous**", None), *((t, t) for t in TYPES)]:
        s = summarize(report.results, type_)
        lines.append(f"| {label} | {s['R']} | {s['E']} | {s['I']} |")
    lines += [
        "",
        "### Répartition des diagnostics",
        "",
        "| Diagnostic | Famille | Nb |",
        "|---|---|---|",
    ]
    counts = Counter(r.diagnostic for r in report.results)
    for diagnostic, n in counts.most_common():
        lines.append(f"| {diagnostic.libelle} | {diagnostic.famille.value} | {n} |")
    lines.append("")
    return "\n".join(lines)


def _render_chunks(result: QuestionResult) -> list[str]:
    """Chunks e2e récupérés ; texte intégral pour sans_reponse, extrait sinon."""

    if not result.chunks:
        return ["Chunks e2e : aucun"]
    lines = ["Chunks e2e récupérés :", ""]
    for rank, chunk in enumerate(result.chunks, 1):
        texte = " ".join(chunk.text.split())
        if result.type != "sans_reponse" and len(texte) > EXTRAIT_CHARS:
            texte = texte[:EXTRAIT_CHARS] + "…"
        lines.append(
            f"{rank}. `{chunk.doc_id}` #{chunk.chunk_index} (score {chunk.score}) — {texte}"
        )
    return lines


def render_question(result: QuestionResult) -> str:
    """Section d'une question : R, E, I, diagnostic, détail et chunks e2e."""

    lines = [f"### {result.id} ({result.type})", ""]
    if result.error is not None:
        lines += [f"- **ERREUR d'I/O** : {result.error}", ""]
        return "\n".join(lines)
    if result.retrieval is None:
        retrieval = "N/A"
    else:
        retrieval = "OK" if result.retrieval.ok else "KO"
        if result.retrieval.docs_manquants:
            retrieval += f" — documents manquants : {result.retrieval.docs_manquants}"
        if result.retrieval.points_absents:
            retrieval += f" — points absents des chunks : {result.retrieval.points_absents}"
    lines += [
        f"- retrieval : {retrieval}",
        f"- end_to_end : {_verdict(result.e2e)}",
        f"- isolated : {_verdict(result.isolated)}",
        f"- diagnostic : {result.diagnostic.libelle} ({result.diagnostic.famille.value})"
        f" — à corriger : {result.diagnostic.correction}",
        "",
    ]
    for label, score in (("e2e", result.e2e), ("isolé", result.isolated)):
        if score is not None and not score.passed:
            ko = [pid for pid, ok in score.details.items() if not ok]
            lines.append(f"Points en échec ({label}) : {ko}")
    lines += ["", *_render_chunks(result), ""]
    return "\n".join(lines)


def render_report(report: Report) -> str:
    """Rapport markdown complet."""

    parts = [render_header(report), render_summary(report), "## Détail par question", ""]
    parts += [render_question(r) for r in report.results]
    return "\n".join(parts)


def write_report(report: Report, directory: Path) -> Path:
    """Écrit le rapport dans le dossier donné, un fichier par run."""

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / report_filename(report)
    path.write_text(render_report(report), encoding="utf-8")
    return path
