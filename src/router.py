"""Routage de la question utilisateur vers le pipeline SQL ou RAG."""

from typing import Literal, cast

import anthropic

from src import config

_SYSTEM_PROMPT = """\
Tu es un routeur pour un assistant spécialisé en prévoyance collective d'entreprise.
Tu dois classifier la question de l'utilisateur en exactement un de ces deux types :

- sql : question sur des données chiffrées (montants, effectifs, cotisations, dossiers,
  paiements, contrats) requérant une requête sur la base DuckDB.
- rag : question sur des documents, des règles, des garanties, des définitions ou des procédures.

Réponds uniquement par le mot "sql" ou le mot "rag", sans ponctuation ni explication.\
"""


def route(question: str) -> Literal["sql", "rag"]:
    """Retourne 'sql' ou 'rag' selon la nature de la question."""

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=config.MODEL,
        max_tokens=16,
        temperature=0,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )
    text_block = response.content[0]
    assert isinstance(text_block, anthropic.types.TextBlock)
    label = text_block.text.strip().lower()
    if label not in ("sql", "rag"):
        raise ValueError(f"Réponse inattendue du routeur : {label!r}")
    return cast(Literal["sql", "rag"], label)
