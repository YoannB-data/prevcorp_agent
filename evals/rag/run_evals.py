"""Runner d'éval RAG : rejoue les questions du YAML et écrit un rapport markdown versionné."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.evaluation.report import render_summary, write_report
from src.rag.evaluation.runner import run_eval

EVAL_FILE = Path(__file__).parent / "eval_set.yml"
REPORTS_DIR = Path(__file__).parent / "reports"
DEFAULT_K = 5


def main() -> int:
    """Lance un run complet et retourne un code de sortie non nul en cas d'erreur d'I/O."""

    parser = argparse.ArgumentParser(description="Runner d'éval RAG PrevCorp")
    parser.add_argument("--yaml", type=Path, default=EVAL_FILE, help="fichier de questions")
    parser.add_argument("--k", type=int, default=DEFAULT_K, help="taille du top-k du retrieval")
    parser.add_argument(
        "--variant",
        choices=["header"],
        default="header",
        help="variante d'ingestion attendue, vérifiée contre la collection",
    )
    parser.add_argument("--judge-model", default=None, help="modèle du juge (défaut : JUDGE_MODEL)")
    parser.add_argument("--ids", nargs="*", metavar="ID", help="IDs à évaluer (ex: RC01 RC17)")
    args = parser.parse_args()

    # import paresseux : ouvre Voyage et Qdrant local (verrou disque)
    from src.rag.evaluation.adapters import TEMPERATURE, build_deps, check_variant

    try:
        deps = build_deps(args.judge_model)
        check_variant(args.variant, deps.collection_variant)
    except ValueError as exc:
        # Guard - un label de variante faux produirait un rapport trompeur
        print(f"Éval annulée : {exc}", file=sys.stderr)
        return 2
    report = run_eval(
        args.yaml,
        args.k,
        args.variant,
        retrieve=deps.retrieve,
        generate=deps.generate,
        fetch_doc_chunks=deps.fetch_doc_chunks,
        judge=deps.judge,
        valid_doc_ids=deps.valid_doc_ids,
        model=deps.model,
        judge_model=deps.judge_model,
        temperature=TEMPERATURE,
        ids=args.ids,
    )
    path = write_report(report, REPORTS_DIR)
    print(render_summary(report))
    print(f"Rapport : {path}")
    return 1 if any(r.error for r in report.results) else 0


if __name__ == "__main__":
    sys.exit(main())
