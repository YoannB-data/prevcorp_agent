"""Juge LLM : coche des propositions oui/non, ne note jamais librement."""

import json
import re
from typing import Protocol

import anthropic

from src.rag.eval_schema import Point, RagQuestion

JUDGE_MAX_TOKENS = 512

JUDGE_SYSTEM_PROMPT = """Tu es un correcteur strict. On te donne une question, une réponse \
à évaluer et une liste de propositions numérotées par identifiant.
Pour CHAQUE proposition, réponds true si la réponse l'AFFIRME explicitement, false sinon.
Règles :
- Une proposition niée, contredite ou attribuée au mauvais document n'est pas affirmée (false).
- Les valeurs doivent être rattachées au bon document ou à la bonne garantie si la proposition \
le précise.
- Ne note rien d'autre : pas de commentaire, pas de score.
Réponds uniquement par un objet JSON {"<id>": true|false, ...} couvrant tous les identifiants."""


class Judge(Protocol):
    """Évalue si une réponse affirme chaque proposition fournie."""

    def evaluate(
        self, question: RagQuestion, answer_text: str, points: list[Point]
    ) -> dict[str, bool]:
        """Retourne, pour chaque id de point, True si la réponse l'affirme."""
        ...


class AnthropicJudge:
    """Juge branché sur l'API Anthropic, temperature=0, sortie JSON stricte."""

    def __init__(self, client: anthropic.Anthropic, model: str) -> None:
        """Mémorise le client et le modèle du juge."""

        self.client = client
        self.model = model

    def evaluate(
        self, question: RagQuestion, answer_text: str, points: list[Point]
    ) -> dict[str, bool]:
        """Demande au modèle de cocher chaque proposition, puis valide strictement la sortie."""

        propositions = "\n".join(f"- {p.id} : {p.texte}" for p in points)
        user_message = (
            f"Question : {question.question}\n\n"
            f"Réponse à évaluer :\n{answer_text}\n\n"
            f"Propositions :\n{propositions}"
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=JUDGE_MAX_TOKENS,
            temperature=0,
            system=JUDGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        block = response.content[0]
        assert isinstance(block, anthropic.types.TextBlock)
        return parse_verdicts(block.text, [p.id for p in points])


def parse_verdicts(raw: str, expected_ids: list[str]) -> dict[str, bool]:
    """Extrait l'objet JSON de la sortie du juge et exige un booléen par id attendu."""

    # tolère un éventuel fence ```json autour de l'objet
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if match is None:
        raise ValueError(f"sortie du juge sans objet JSON : {raw!r}")
    data = json.loads(match.group(0))
    manquants = [pid for pid in expected_ids if not isinstance(data.get(pid), bool)]
    if manquants:
        raise ValueError(f"verdict absent ou non booléen pour {manquants} : {raw!r}")
    return {pid: data[pid] for pid in expected_ids}
