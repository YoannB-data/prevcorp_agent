"""Tests du découpage par article (variante prefix_article), sans appel API."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.rag import ingestion
from src.rag.evaluation.adapters import check_variant
from src.rag.ingestion import chunk_by_article, chunk_text


def _words(n: int, prefix: str = "mot") -> str:
    return " ".join(f"{prefix}{i}" for i in range(n))


def test_trois_articles_et_preambule():
    text = (
        f"Préambule\n{_words(20)}\n"
        f"Article 1 — Objet\n{_words(30, 'a')}\n"
        f"Article 2 — Durée\n{_words(30, 'b')}\n"
        f"Article 3 — Fin\n{_words(30, 'c')}\n"
    )
    chunks = chunk_by_article(text)
    assert len(chunks) == 4
    assert chunks[0].startswith("Préambule")
    assert [c.split(" — ")[0] for c in chunks[1:]] == ["Article 1", "Article 2", "Article 3"]
    assert "b0" in chunks[2] and "a0" not in chunks[2]


def test_article_trop_long_redecoupe_avec_titre_repete():
    text = f"Article 1 — Court\n{_words(40)}\nArticle 2 — Très long\n{_words(400, 'x')}\n"
    chunks = chunk_by_article(text)
    long_chunks = [c for c in chunks if c.startswith("Article 2 — Très long")]
    assert len(long_chunks) > 1
    assert all(c.startswith("Article 2 — Très long x") for c in long_chunks)
    assert chunks[0].startswith("Article 1 — Court")
    assert len(chunks) == 1 + len(long_chunks)


def test_texte_sans_article_garde_le_decoupage_historique():
    text = _words(400)
    assert chunk_by_article(text) == chunk_text(text)


def test_reference_a_un_article_en_milieu_de_ligne_ne_coupe_pas():
    text = f"Article 1 — Objet\n{_words(10)} voir Article 2 — ailleurs {_words(10)}\n"
    assert len(chunk_by_article(text)) == 1


def test_ingest_pdf_prefix_article_utilise_le_decoupage_par_article(monkeypatch):
    monkeypatch.setattr(ingestion, "extract_text", lambda _p: "texte")
    monkeypatch.setattr(
        ingestion,
        "chunk_by_article",
        lambda _t: ["Article 1 — A", "Article 2 — B"],
    )
    monkeypatch.setattr(ingestion, "document_prefix", lambda *_: "[préfixe]")
    voyage = MagicMock()
    voyage.embed.side_effect = lambda texts, **_: SimpleNamespace(
        embeddings=[[0.0] * 3] * len(texts)
    )
    counts = ingestion.ingest_pdf(Path("REGLEMENT_x.pdf"), voyage, MagicMock(), "prefix_article")
    assert counts == (2, 2)
    embedded = voyage.embed.call_args.args[0]
    assert embedded == ["[préfixe]\nArticle 1 — A", "[préfixe]\nArticle 2 — B"]


def test_check_variant_refuse_prefix_article_sur_collection_prefix():
    with pytest.raises(ValueError, match="--variant prefix_article.*'prefix'"):
        check_variant("prefix_article", "prefix")
    check_variant("prefix_article", "prefix_article")
