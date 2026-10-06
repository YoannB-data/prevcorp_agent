"""Tests de l'inférence du type de document depuis le nom de fichier."""

import pytest

from src.rag.metadata import doc_type_from_filename


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("REGLEMENT_prevcorp.pdf", "reglement"),
        ("NOTICE_CCN_metallurgie.pdf", "notice_ccn"),
        ("NOTICE_CCN_metallurgie_distracteur.pdf", "notice_ccn"),
        ("RESUME_C87656.pdf", "resume_contrat"),
        ("FAQ_prevcorp.pdf", "faq"),
        ("resume_c87656.pdf", "resume_contrat"),
        ("inconnu.pdf", "autre"),
    ],
)
def test_doc_type_from_filename(filename, expected):
    """Vérifie le type inféré pour chaque préfixe, la casse et le cas inconnu."""

    assert doc_type_from_filename(filename) == expected
