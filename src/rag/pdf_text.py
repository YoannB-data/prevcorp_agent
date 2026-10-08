"""Extraction du texte d'un PDF du corpus (sans client externe, importable en test)."""

from pathlib import Path

import pdfplumber


def extract_text(pdf_path: Path) -> str:
    """Extrait texte + tableaux d'un PDF, en traitant les tableaux séparément."""

    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            blocks = []
            # Tableaux
            for table in page.extract_tables():
                if not table:
                    continue
                header = table[0]
                rows = table[1:]
                table_lines = [" | ".join(str(c) for c in header)]
                table_lines += [" | ".join(str(c) for c in row) for row in rows]
                blocks.append("\n".join(table_lines))
            # Texte hors tableaux
            text = page.extract_text()
            if text:
                blocks.append(text.strip())
            pages_text.append("\n\n".join(blocks))
    return "\n\n".join(pages_text)
