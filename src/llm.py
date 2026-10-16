"""Utilitaires partagés pour lire les réponses de l'API Anthropic."""

from typing import Any


def extract_text(response: Any) -> str:
    """Texte du premier bloc `text` ; ValueError si la réponse n'en contient aucun."""

    for block in response.content:
        if block.type == "text":
            return str(block.text)
    # Guard - un modèle qui raisonne peut ne renvoyer aucun bloc text (ex. tronqué par max_tokens)
    types = [block.type for block in response.content]
    raise ValueError(
        f"réponse sans bloc text : blocs={types}, stop_reason={response.stop_reason!r}"
    )
