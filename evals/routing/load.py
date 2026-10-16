"""Chargement et validation de l'eval set de routing."""

from collections import Counter
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict

Route = Literal["sql", "rag", "hybride"]
Forme = Literal["simple", "explicite", "implicite", "dependante", "piege"]

EVAL_FILE = Path(__file__).parent / "eval_set.yml"


class RoutingCase(BaseModel):
    """Une question de routing avec sa route attendue."""

    # extra=forbid : une faute de frappe dans un nom de champ doit lever, pas passer en silence
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    question: str
    route_attendue: Route
    forme: Forme
    origine: str
    note: str
    reponse_attendue: str | None = None


class Seuils(BaseModel):
    """Seuils de décision du bloc meta."""

    model_config = ConfigDict(extra="forbid")

    accuracy: float
    rappel_hybride: float


class EvalSet(BaseModel):
    """Eval set chargé : questions validées et seuils."""

    cases: list[RoutingCase]
    seuils: Seuils


def load_eval_set(path: Path = EVAL_FILE) -> EvalSet:
    """Charge le YAML ; schéma invalide : ValidationError, ID dupliqué : ValueError."""

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    cases = [RoutingCase.model_validate(q) for q in raw["questions"]]
    duplicates = sorted(i for i, n in Counter(c.id for c in cases).items() if n > 1)
    if duplicates:
        raise ValueError(f"IDs dupliqués dans {path.name} : {duplicates}")
    return EvalSet(cases=cases, seuils=Seuils.model_validate(raw["meta"]["seuils"]))
