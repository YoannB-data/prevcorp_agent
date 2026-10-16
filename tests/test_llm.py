"""Tests de l'extraction du texte d'une réponse de l'API."""

from types import SimpleNamespace

import pytest

from src.llm import extract_text


def _block(type_: str, **kw):
    return SimpleNamespace(type=type_, **kw)


def _response(blocks, stop_reason="end_turn"):
    return SimpleNamespace(content=blocks, stop_reason=stop_reason)


def test_reponse_texte_seul():
    """Un seul bloc text : son texte est renvoyé."""

    assert extract_text(_response([_block("text", text="SELECT 1")])) == "SELECT 1"


def test_reponse_thinking_puis_text():
    """Le bloc thinking en tête est ignoré."""

    resp = _response([_block("thinking", thinking="..."), _block("text", text="SELECT 1")])
    assert extract_text(resp) == "SELECT 1"


def test_reponse_sans_bloc_text_leve_avec_types_et_stop_reason():
    """L'erreur nomme les blocs reçus et le stop_reason."""

    resp = _response([_block("thinking", thinking="...")], stop_reason="max_tokens")
    with pytest.raises(ValueError, match=r"blocs=\['thinking'\], stop_reason='max_tokens'"):
        extract_text(resp)
