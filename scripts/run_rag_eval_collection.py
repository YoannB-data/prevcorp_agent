"""Lance le runner d'éval RAG sur une collection Qdrant autre que celle du retriever."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "evals" / "rag"))


def main() -> int:
    """Remplace COLLECTION_NAME du retriever (sans le modifier) puis délègue à run_evals."""

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--collection", required=True)
    args, rest = parser.parse_known_args()

    from src.rag import retriever

    retriever.COLLECTION_NAME = args.collection
    import run_evals

    sys.argv = ["run_evals.py", *rest]
    return run_evals.main()


if __name__ == "__main__":
    sys.exit(main())
