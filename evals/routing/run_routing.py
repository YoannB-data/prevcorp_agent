"""Runner d'éval du routeur : N runs, métriques agrégées, rapport markdown horodaté."""

import argparse
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evals.routing import metrics
from evals.routing.load import EVAL_FILE, EvalSet, Route, load_eval_set

REPORTS_DIR = Path(__file__).parent / "reports"


@dataclass(frozen=True)
class Prediction:
    """Route prédite pour une question lors d'un run, et latence mesurée."""

    predicted: str
    latency_s: float


def run_once(eval_set: EvalSet, route_fn: Callable[[str], str]) -> list[Prediction]:
    """Route chaque question une fois ; seule une réponse hors sql/rag devient « erreur »."""

    results = []
    for case in eval_set.cases:
        start = time.perf_counter()
        try:
            predicted = route_fn(case.question)
        except ValueError:
            # Catch-all - seule une réponse hors sql/rag est une erreur de routage ; l'API plante
            predicted = metrics.ERREUR
        results.append(Prediction(predicted, time.perf_counter() - start))
    return results


def _git_hash() -> str:
    """Hash court du commit courant, « inconnu » hors dépôt."""

    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return "inconnu"
    return out.stdout.strip()


def _ok(value: float, seuil: float) -> str:
    """Verdict OK/KO d'une valeur contre son seuil."""

    return "OK" if value >= seuil else "KO"


def render_report(
    eval_set: EvalSet, runs: list[list[Prediction]], *, model: str, commit: str, date: str
) -> str:
    """Construit le rapport markdown à partir des prédictions de tous les runs."""

    cases = eval_set.cases
    per_run = [[(c.route_attendue, p.predicted) for c, p in zip(cases, run)] for run in runs]
    flat = [pair for run in per_run for pair in run]
    classes: tuple[Route, ...] = ("hybride", "sql", "rag")  # rappel hybride en premier

    lines = [
        "# Rapport d'éval du routeur",
        "",
        f"- Modèle : `{model}`",
        f"- Commit : `{commit}`",
        f"- Runs : {len(runs)}",
        f"- Date : {date}",
        f"- Questions : {len(cases)}",
        "",
        "## Accuracy globale",
        "",
    ]
    accs = [metrics.accuracy(pairs) for pairs in per_run]
    mean, lo, hi = metrics.mean_min_max(accs)
    lines.append(f"Moyenne {mean:.1%} (min {lo:.1%} – max {hi:.1%}) sur {len(runs)} run(s).")

    recalls = {c: metrics.recall(flat, c) for c in classes}
    hybride_recall = recalls["hybride"]
    lines += ["", "## Seuils (meta)", ""]
    lines += ["| Métrique | Valeur | Seuil | Verdict |", "|---|---|---|---|"]
    lines.append(
        f"| accuracy (moyenne) | {mean:.1%} | {eval_set.seuils.accuracy:.0%} "
        f"| {_ok(mean, eval_set.seuils.accuracy)} |"
    )
    seuil_h = eval_set.seuils.rappel_hybride
    verdict = "KO" if hybride_recall is None else _ok(hybride_recall, seuil_h)
    lines.append(
        f"| rappel hybride | {metrics.fmt_ratio(hybride_recall)} "
        f"| {eval_set.seuils.rappel_hybride:.0%} | {verdict} |"
    )

    lines += ["", "## Rappel et précision par classe (runs cumulés)", ""]
    lines += ["| Classe | Rappel | Précision |", "|---|---|---|"]
    for cls in classes:
        lines.append(
            f"| {cls} | {metrics.fmt_ratio(recalls[cls])} "
            f"| {metrics.fmt_ratio(metrics.precision(flat, cls))} |"
        )

    lines += ["", "## Matrice de confusion (runs cumulés, lignes = attendu, colonnes = prédit)", ""]
    matrix = metrics.confusion_matrix(flat)
    lines += ["| attendu \\ prédit | sql | rag | hybride |", "|---|---|---|---|"]
    for expected in metrics.ROUTES:
        row = matrix[expected]
        lines.append(f"| {expected} | {row['sql']} | {row['rag']} | {row['hybride']} |")

    lines += ["", "## Accuracy par forme (runs cumulés)", ""]
    lines += ["| Forme | n | Correctes | Accuracy |", "|---|---|---|---|"]
    triples = [(c.forme, c.route_attendue, p.predicted) for run in runs for c, p in zip(cases, run)]
    stats = metrics.accuracy_by_forme(triples, len(cases) * len(runs))
    for forme, st in stats.items():
        lines.append(f"| {forme} | {st.n} | {st.correct} | {metrics.fmt_ratio(st.accuracy)} |")
    total = sum(st.n for st in stats.values())
    ok = sum(st.correct for st in stats.values())
    lines.append(f"| **Total** | {total} | {ok} | {metrics.fmt_ratio(ok / total)} |")

    by_id = {c.id: [run[i].predicted for run in runs] for i, c in enumerate(cases)}
    unstable = metrics.unstable_ids(by_id)
    lines += ["", f"## Questions instables ({len(unstable)})", ""]
    lines += [f"- {qid} : {' / '.join(by_id[qid])}" for qid in unstable] or ["Aucune."]

    errors = [
        (c.id, i + 1)
        for i, run in enumerate(runs)
        for c, p in zip(cases, run)
        if p.predicted == metrics.ERREUR
    ]
    lines += ["", f"## Réponses hors sql/rag ({len(errors)})", ""]
    lines += [f"- {qid} (run {n})" for qid, n in errors] or ["Aucune."]

    latencies = [p.latency_s for run in runs for p in run]
    lines += [
        "",
        "## Latence et coût",
        "",
        f"- Latence par question : moyenne {sum(latencies) / len(latencies):.2f} s, "
        f"max {max(latencies):.2f} s. Mesurée par le runner autour de `route()` ; "
        "elle inclut la création du client Anthropic.",
        "- Coût et tokens : non exposés par le routeur.",
        "",
        "## Erreurs de routage (dernier run)",
        "",
    ]
    wrong = [
        f"- {c.id} [{c.forme}] attendu {c.route_attendue}, prédit {p.predicted}"
        for c, p in zip(cases, runs[-1])
        if c.route_attendue != p.predicted
    ]
    lines += wrong or ["Aucune."]
    return "\n".join(lines) + "\n"


def main() -> int:
    """Lance les runs, écrit le rapport horodaté et l'affiche."""

    parser = argparse.ArgumentParser(description="Runner d'éval du routeur PrevCorp")
    parser.add_argument("--runs", type=int, default=3, help="nombre de runs")
    parser.add_argument("--yaml", type=Path, default=EVAL_FILE, help="fichier de questions")
    args = parser.parse_args()
    # Guard - un nombre de runs nul produirait des moyennes sur rien
    if args.runs < 1:
        print("--runs doit être >= 1", file=sys.stderr)
        return 2

    # import paresseux : src.config exige les variables d'environnement
    from src import config
    from src.router import route

    eval_set = load_eval_set(args.yaml)
    runs = [run_once(eval_set, route) for _ in range(args.runs)]
    now = datetime.now()
    report = render_report(
        eval_set,
        runs,
        model=config.ROUTER_MODEL,
        commit=_git_hash(),
        date=now.strftime("%Y-%m-%d %H:%M:%S"),
    )
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"routing_{now.strftime('%Y%m%d_%H%M%S')}.md"
    path.write_text(report, encoding="utf-8")
    print(report)
    print(f"Rapport : {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
