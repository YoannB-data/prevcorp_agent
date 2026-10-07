"""Tests du diagnostic R/E/I (pur, sans I/O)."""

import pytest

from src.rag.evaluation.diagnose import diagnose
from src.rag.evaluation.models import Diagnostic, Famille


@pytest.mark.parametrize(
    ("r", "e", "i", "attendu", "famille"),
    [
        (True, True, True, Diagnostic.SAIN, Famille.SUCCES),
        (True, False, True, Diagnostic.BRUIT_TOP_K, Famille.ECHEC),
        (True, False, False, Diagnostic.ECHEC_GENERATION, Famille.ECHEC),
        (False, False, True, Diagnostic.ECHEC_RETRIEVAL, Famille.ECHEC),
        (False, False, False, Diagnostic.DOUBLE_ECHEC, Famille.ECHEC),
        (False, True, True, Diagnostic.SUCCES_SANS_SOURCE, Famille.SUSPECT),
        (False, True, False, Diagnostic.SUCCES_SANS_SOURCE_ISOLE_KO, Famille.SUSPECT),
        (True, True, False, Diagnostic.E2E_OK_ISOLE_KO, Famille.SUSPECT),
    ],
)
def test_cube_complet(r, e, i, attendu, famille):
    assert diagnose(r, e, i) is attendu
    assert attendu.famille is famille


@pytest.mark.parametrize(
    ("e", "i", "attendu", "famille"),
    [
        (True, True, Diagnostic.SAIN, Famille.SUCCES),
        (False, True, Diagnostic.ALERTE_CHUNK_TENTANT, Famille.ALERTE),
        (False, False, Diagnostic.ECHEC_GENERATION_OU_PIEGE, Famille.ECHEC),
        (True, False, Diagnostic.SUSPECT_SANS_REPONSE, Famille.SUSPECT),
    ],
)
def test_sans_reponse(e, i, attendu, famille):
    assert diagnose(None, e, i) is attendu
    assert attendu.famille is famille
