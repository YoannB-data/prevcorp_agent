"""Sélection et formatage d'exemples few-shot pour le prompt agent."""

from pathlib import Path

import yaml


def _load_few_shot_bank() -> list[dict]:
    """Charge tous les exemples depuis few_shot_bank.yml."""

    path = Path(__file__).parent / "prompts" / "few_shot_bank.yml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)["examples"]


def select_examples(question: str, n: int = 2) -> list[dict]:
    """Retourne les n exemples dont les mots-clés matchent le mieux la question."""

    examples = _load_few_shot_bank()
    question_lower = question.lower()
    scored = sorted(
        examples,
        key=lambda ex: sum(kw in question_lower for kw in ex["keywords"]),
        reverse=True,
    )
    matched = [
        ex for ex in scored if any(kw in question_lower for kw in ex["keywords"])
    ]
    return matched[:n]


def format_few_shot(examples: list[dict]) -> str:
    """Formate une liste d'exemples en bloc Markdown prêt à injecter dans le prompt."""

    if not examples:
        return ""
    lines = ["# Exemples de requêtes similaires :"]
    for ex in examples:
        lines.append(f"Question : {ex['question']}")
        lines.append(f"```sql\n{ex['sql'].strip()}\n```")
        lines.append("")
    return "\n".join(lines)
