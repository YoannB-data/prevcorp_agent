"""Rendu HTML vers PDF pour le corpus PrevCorp, via weasyprint (avec fallback Edge headless)."""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

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


def _weasyprint_available() -> bool:
    """Vérifie si weasyprint peut être importé (GTK3/Pango disponibles)."""

    try:
        import weasyprint  # noqa: F401
    except (ImportError, OSError):
        # Catch-all - weasyprint non installé, ou GTK3/Pango absent (Windows sans le runtime)
        return False
    return True


def _render_with_weasyprint(html_path: Path, output_path: Path) -> None:
    """Convertit un HTML en PDF via weasyprint."""

    from weasyprint import HTML

    HTML(filename=str(html_path)).write_pdf(str(output_path))


def _render_with_edge_fallback(html_path: Path, output_path: Path) -> None:
    """Convertit un HTML en PDF via Edge headless, en secours quand weasyprint est indisponible."""

    edge_binary = os.environ.get(
        "EDGE_BINARY", "msedge"
    )  # Surchargeable si msedge n'est pas sur le PATH
    resolved_output = (
        output_path.resolve()
    )  # Guard - un chemin relatif fait échouer Edge silencieusement (code 0, rien écrit)
    command = [
        edge_binary,
        "--headless",
        "--disable-gpu",
        # Sans ce flag, Edge injecte date/titre/chemin dans chaque page, donc dans les chunks
        "--no-pdf-header-footer",
        f"--print-to-pdf={resolved_output}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        # Catch-all - normalise l'échec Edge en erreur explicite pour l'appelant
        raise RuntimeError(f"Edge headless a échoué (code {result.returncode}) : {result.stderr}")
    if not resolved_output.exists() or resolved_output.stat().st_size == 0:
        # Guard - Edge peut rendre un code 0 sans avoir rien écrit (ex : chemin de sortie invalide)
        raise RuntimeError(
            f"Edge headless a rendu un succès mais {resolved_output} est absent ou vide."
        )


def render(
    html_path: Path, doc_type: str, identifiant: str, corpus_dir: Path = Path("corpus")
) -> Path:
    """Convertit un fichier HTML en PDF et l'écrit dans le corpus avec le nom conventionnel."""

    corpus_dir.mkdir(
        exist_ok=True
    )  # Guard - le dossier corpus/ peut ne pas exister au premier lancement
    output_path = corpus_dir / build_filename(doc_type, identifiant)

    if _weasyprint_available():
        _render_with_weasyprint(html_path, output_path)
    else:
        print("weasyprint indisponible (GTK3 manquant) — rendu via Edge headless en secours.")
        _render_with_edge_fallback(html_path, output_path)

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
