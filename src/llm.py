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


def extract_thinking_tokens(response: Any) -> int:
    """Tokens de raisonnement (inclus dans output_tokens) ; 0 si l'API ne les expose pas."""

    details = getattr(response.usage, "output_tokens_details", None)
    # Le SDK renvoie parfois un dict, parfois un objet typé
    if isinstance(details, dict):
        return int(details.get("thinking_tokens") or 0)
    return int(getattr(details, "thinking_tokens", 0) or 0)
