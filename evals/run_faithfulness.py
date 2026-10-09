"""Faithfulness maison sur les questions RAG : variante prefix, rapport markdown versionné."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.eval_schema import load_questions
from src.rag.evaluation.faithfulness import (
    FaithfulnessRow,
    render_report,
    report_filename,
    score_faithfulness,
    write_report,
)
from src.rag.evaluation.report import hash_yaml

EVAL_FILE = Path(__file__).parent / "rag_questions_v1_25.yml"
REPORTS_DIR = Path(__file__).parent / "reports" / "rag"
DEFAULT_K = 5
VARIANT = "prefix"


def main() -> int:
    """Lance le run et retourne 2 si la collection n'est pas en prefix, 1 en cas d'erreur d'I/O."""

    parser = argparse.ArgumentParser(description="Faithfulness maison PrevCorp")
    parser.add_argument("--yaml", type=Path, default=EVAL_FILE, help="fichier de questions")
    parser.add_argument("--k", type=int, default=DEFAULT_K, help="taille du top-k du retrieval")
    parser.add_argument("--judge-model", default=None, help="modèle du juge (défaut : MODEL)")
    parser.add_argument("--ids", nargs="*", metavar="ID", help="IDs à évaluer (ex: RC01 RC25)")
    args = parser.parse_args()

    # import paresseux : ouvre Voyage et Qdrant local (verrou disque)
    from src.rag.evaluation.adapters import build_deps, check_variant

    try:
        deps = build_deps(args.judge_model)
        check_variant(VARIANT, deps.collection_variant)
        questions = load_questions(args.yaml, deps.valid_doc_ids)
    except ValueError as exc:
        # Guard - un score sur la mauvaise variante produirait un rapport trompeur
        print(f"Éval annulée : {exc}", file=sys.stderr)
        return 2
    if args.ids:
        questions = [q for q in questions if q.id in args.ids]

    rows: list[FaithfulnessRow] = []
    for q in questions:
        try:
            chunks = deps.retrieve(q.question, args.k)
            answer = deps.generate(q.question, chunks).text
            result = score_faithfulness(deps.judge, q.question, answer, chunks)
            row = FaithfulnessRow(
                id=q.id,
                type=q.type,
                score=result.score,
                n_claims=len(result.claims),
                unsupported=result.unsupported,
                answer=answer,
            )
        except Exception as exc:
            # Catch-all - une erreur d'I/O sur une question ne doit pas perdre le run
            row = FaithfulnessRow(id=q.id, type=q.type, error=f"{type(exc).__name__}: {exc}")
        rows.append(row)
        print(f"{row.id} : {row.error or row.score}")

    now = datetime.now()
    yaml_hash = hash_yaml(args.yaml)
    content = render_report(
        rows,
        date=now,
        yaml_hash=yaml_hash,
        model=deps.model,
        judge_model=deps.judge_model,
        k=args.k,
        variant=VARIANT,
    )
    path = write_report(content, REPORTS_DIR, report_filename(now, VARIANT, yaml_hash))
    print(f"Rapport : {path}")
    return 1 if any(r.error for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
