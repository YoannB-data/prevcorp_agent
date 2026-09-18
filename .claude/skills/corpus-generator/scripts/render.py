"""Rendu HTML vers PDF pour le corpus PrevCorp, via weasyprint."""

import sys
from pathlib import Path

from weasyprint import HTML

_TYPE_PREFIXES = {
    "reglement": "REGLEMENT",
    "notice_ccn": "NOTICE_CCN",
    "resume_garanties": "RESUME",
    "faq": "FAQ",
}


def build_filename(doc_type: str, identifiant: str) -> str:
    """Construit le nom de fichier selon la convention <TYPE>_<identifiant>.pdf."""

    prefix = _TYPE_PREFIXES.get(doc_type, doc_type.upper())
    return f"{prefix}_{identifiant}.pdf"


def render(
    html_path: Path, doc_type: str, identifiant: str, corpus_dir: Path = Path("corpus")
) -> Path:
    """Convertit un fichier HTML en PDF et l'écrit dans le corpus avec le nom conventionnel."""

    corpus_dir.mkdir(
        exist_ok=True
    )  # Guard - le dossier corpus/ peut ne pas exister au premier lancement
    output_path = corpus_dir / build_filename(doc_type, identifiant)
    HTML(filename=str(html_path)).write_pdf(str(output_path))
    return output_path


def main() -> None:
    """Point d'entrée CLI : html_path, doc_type, identifiant."""

    if len(sys.argv) != 4:
        print("Usage: render.py <html_path> <doc_type> <identifiant>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    doc_type = sys.argv[2]
    identifiant = sys.argv[3]

    output_path = render(html_path, doc_type, identifiant)
    print(f"PDF généré : {output_path}")


if __name__ == "__main__":
    main()
