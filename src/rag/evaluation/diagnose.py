"""Diagnostic du cube R/E/I : fonction pure, sans I/O."""

from src.rag.evaluation.models import Diagnostic

_TABLE_RETRIEVAL: dict[tuple[bool, bool, bool], Diagnostic] = {
    (True, True, True): Diagnostic.SAIN,
    (True, False, True): Diagnostic.BRUIT_TOP_K,
    (True, False, False): Diagnostic.ECHEC_GENERATION,
    (False, False, True): Diagnostic.ECHEC_RETRIEVAL,
    (False, False, False): Diagnostic.DOUBLE_ECHEC,
    (False, True, True): Diagnostic.SUCCES_SANS_SOURCE,
    (False, True, False): Diagnostic.SUCCES_SANS_SOURCE_ISOLE_KO,
    (True, True, False): Diagnostic.E2E_OK_ISOLE_KO,
}

_TABLE_SANS_REPONSE: dict[tuple[bool, bool], Diagnostic] = {
    (True, True): Diagnostic.SAIN,
    (False, True): Diagnostic.ALERTE_CHUNK_TENTANT,
    (False, False): Diagnostic.ECHEC_GENERATION_OU_PIEGE,
    (True, False): Diagnostic.SUSPECT_SANS_REPONSE,
}


def diagnose(retrieval: bool | None, e2e: bool, isolated: bool) -> Diagnostic:
    """Diagnostique une question ; retrieval vaut None quand il est N/A (sans_reponse)."""

    if retrieval is None:
        return _TABLE_SANS_REPONSE[(e2e, isolated)]
    return _TABLE_RETRIEVAL[(retrieval, e2e, isolated)]
