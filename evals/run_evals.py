"""Runner d'évaluation — compare les résultats de l'agent aux requêtes de référence."""

import datetime
import math
from pathlib import Path

import pandas as pd
import yaml

from src.agent import agent_main
from src.duckdb_executor import execute_query

EVAL_FILE = Path(__file__).parent / "eval_set.yml"


def _compare_scalar(df_a: pd.DataFrame, df_r: pd.DataFrame) -> tuple[bool, str]:
    """Compare une valeur scalaire unique, avec tolérance flottante si possible."""

    val_a = df_a.iloc[0, 0]
    val_r = df_r.iloc[0, 0]
    try:
        passed = math.isclose(float(val_a), float(val_r), rel_tol=1e-6)
    except (TypeError, ValueError):
        passed = val_a == val_r
    if passed:
        return True, ""
    return False, f"agent={val_a}, ref={val_r}"


def _compare_row_count(df_a: pd.DataFrame, df_r: pd.DataFrame) -> tuple[bool, str]:
    """Compare uniquement le nombre de lignes, sans regarder les valeurs."""

    if len(df_a) == len(df_r):
        return True, ""
    return False, f"agent={len(df_a)} lignes, ref={len(df_r)} lignes"


def _compare_key_set(
    df_a: pd.DataFrame, df_r: pd.DataFrame, key_column: str
) -> tuple[bool, str]:
    """Compare les ensembles de clés sans tenir compte de l'ordre ni des doublons."""

    set_a = set(df_a[key_column])
    set_r = set(df_r[key_column])
    if set_a == set_r:
        return True, ""
    missing = set_r - set_a
    extra = set_a - set_r
    return False, f"manquants={missing}, en_trop={extra}"


def _compare_exact_sorted(
    df_a: pd.DataFrame, df_r: pd.DataFrame, _key_column: str
) -> tuple[bool, str]:
    """Compare valeurs et ordre exact, rapporte les lignes divergentes."""

    if df_a.shape != df_r.shape:
        return False, f"shape: agent={df_a.shape}, ref={df_r.shape}"
    if df_a.values.tolist() == df_r.values.tolist():
        return True, ""
    diffs = []
    for i, (row_a, row_r) in enumerate(zip(df_a.values.tolist(), df_r.values.tolist())):
        if row_a != row_r:
            diffs.append(f"ligne {i}: agent={row_a}, ref={row_r}")
    return False, " | ".join(diffs)


def _compare(
    compare: str,
    key_column: str | None,
    df_agent: pd.DataFrame,
    df_ref: pd.DataFrame,
) -> tuple[bool, str]:
    """Dispatche vers la fonction de comparaison adaptée au mode demandé."""

    match compare:
        case "scalar":
            return _compare_scalar(df_agent, df_ref)
        case "row_count":
            return _compare_row_count(df_agent, df_ref)
        case "key_set":
            return _compare_key_set(df_agent, df_ref, key_column)
        case "exact_sorted":
            return _compare_exact_sorted(df_agent, df_ref, key_column)
        case _:
            return False, f"mode de comparaison inconnu : {compare}"


def run_single_eval(item: dict) -> dict:
    """Évalue une question et retourne un dict avec id, question, status et detail."""

    qid = item["id"]
    question = item["question"]
    compare = item.get("compare", "skip")
    key_column = item.get("key_column")
    reference_sql = item.get("reference_sql", "")

    if compare == "skip":
        return {"id": qid, "question": question, "status": "SKIP", "detail": ""}

    try:
        df_agent = agent_main(question, eval_question_id=qid)
        df_ref = execute_query(reference_sql)
        passed, detail = _compare(compare, key_column, df_agent, df_ref)
        return {
            "id": qid,
            "question": question,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
    except Exception as e:  # pylint: disable=broad-exception-caught
        return {"id": qid, "question": question, "status": "ERROR", "detail": str(e)}


# ─────────────────────────────────────────────
# Rapport Markdown
# ─────────────────────────────────────────────


def write_report(results: list[dict]) -> None:
    """Écrit le rapport d'évaluation dans evals/reports/report_YYYYMMDD_HHMMSS.md."""

    now = datetime.datetime.now()
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"report_{now.strftime('%Y%m%d_%H%M%S')}.md"

    skipped = sum(1 for r in results if r["status"] == "SKIP")
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)

    lines = [
        f"# Rapport d'évaluation — {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"**Score : {passed}/{total - skipped} PASS**  ",
        "",
        "| Statut | Nombre |",
        "|--------|--------|",
    ]
    for status in ("PASS", "FAIL", "ERROR", "SKIP"):
        lines.append(
            f"| {status} | {sum(1 for r in results if r['status'] == status)} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Tableau complet",
        "",
        "| ID | Question | Statut | Détail |",
        "|----|----------|--------|--------|",
    ]
    for r in results:
        detail = r["detail"].replace("|", "\\|")[:120]
        lines.append(f"| {r['id']} | {r['question'][:60]} | {r['status']} | {detail} |")

    lines += ["", "---", "", "## FAIL et ERROR", ""]
    failures = [r for r in results if r["status"] in ("FAIL", "ERROR")]
    if failures:
        for r in failures:
            lines += [
                f"### {r['id']} — {r['status']}",
                f"> {r['question']}",
                "",
                r["detail"],
                "",
            ]
    else:
        lines.append("_Aucun._")

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nRapport écrit : {path}")


# ─────────────────────────────────────────────
# Runner principal
# ─────────────────────────────────────────────


def run_evals(ids: list[str] | None = None) -> list[dict]:
    """Lance toutes les évaluations (ou une partie), affiche la progression et le résumé final."""

    with open(EVAL_FILE, encoding="utf-8") as f:
        questions = yaml.safe_load(f)["questions"]
    if ids:
        questions = [q for q in questions if q["id"] in ids]
    results = []
    total = len(questions)
    for i, item in enumerate(questions, 1):
        r = run_single_eval(item)
        results.append(r)
        print(f"[{i}/{total}] [{r['status']}] {r['id']} : {r['question'][:70]}")
        if r["detail"]:
            print(f"       {r['detail'][:200]}")

    skipped = sum(1 for r in results if r["status"] == "SKIP")
    passed = sum(1 for r in results if r["status"] == "PASS")
    print("\n" + "=" * 60)
    print(f"RÉSULTATS : {passed}/{len(results) - skipped} PASS")
    for status in ("PASS", "FAIL", "ERROR", "SKIP"):
        print(f"  {status:<6}: {sum(1 for r in results if r['status'] == status)}")
    print("=" * 60)

    write_report(results)
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Runner d'évaluation PrevCorp Agent")
    parser.add_argument(
        "--ids", nargs="*", metavar="ID", help="IDs à évaluer (ex: Q012 Q034)"
    )
    args = parser.parse_args()
    run_evals(ids=args.ids)
