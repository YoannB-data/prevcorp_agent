"""Schéma et chargement fail-fast des questions d'éval RAG (sans client externe)."""

from collections import Counter
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

DISTRACTEUR_ID = "NOTICE_CCN_metallurgie_distracteur"
ID_PATTERN = r"^RC\d{2}$"


class RagQuestion(BaseModel):
    """Une question d'éval RAG et son contrat de données."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=ID_PATTERN)
    question: str
    type: Literal["fait_simple", "chiffre_precis", "croisement", "sans_reponse"]
    contrat_cible: str | None
    reponse_attendue: str
    sources_attendues: list[str]
    contexte_isole: list[str] | None = None
    corpus_a_contenir: str

    @field_validator("question", "reponse_attendue", "corpus_a_contenir")
    @classmethod
    def _non_vide(cls, value: str) -> str:
        """Refuse les textes vides ou blancs."""

        if not value.strip():
            raise ValueError("texte vide")
        return value

    @model_validator(mode="after")
    def _check_rules(self) -> "RagQuestion":
        """Applique les règles métier propres à une question."""

        sources = self.sources_attendues
        # Un run isolé sans contexte est un mauvais run, quel que soit le type
        if self.contexte_isole is not None and not self.contexte_isole:
            raise ValueError("contexte_isole présent mais vide")
        if self.type == "sans_reponse":
            if sources:
                raise ValueError("sans_reponse exige sources_attendues vide")
            if not self.contexte_isole:
                raise ValueError("sans_reponse exige un contexte_isole non vide")
        elif self.type == "croisement":
            if len(set(sources)) < 2:
                raise ValueError("croisement exige au moins 2 sources distinctes")
        elif not sources:
            raise ValueError(f"{self.type} exige au moins 1 source")

        if DISTRACTEUR_ID in sources or DISTRACTEUR_ID in (self.contexte_isole or []):
            raise ValueError(f"{DISTRACTEUR_ID} interdit en source ou contexte_isole")
        doublons = sorted(doc for doc, n in Counter(sources).items() if n > 1)
        if doublons:
            raise ValueError(f"doublons dans sources_attendues : {doublons}")
        return self


def _format_error(exc: ValidationError) -> str:
    """Condense les erreurs Pydantic en une ligne lisible."""

    parts = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"])
        msg = err["msg"].removeprefix("Value error, ")
        parts.append(f"{loc} : {msg}" if loc else msg)
    return " ; ".join(parts)


def load_questions(path: Path, valid_doc_ids: set[str]) -> list[RagQuestion]:
    """Charge et valide les questions du fichier, échoue à la première violation."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    # Guard - la racine doit porter la liste `questions`
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError(f"{path.name} : clé racine 'questions' (liste) manquante")

    questions: list[RagQuestion] = []
    seen: set[str] = set()
    for index, raw in enumerate(data["questions"]):
        label = raw.get("id", f"#{index}") if isinstance(raw, dict) else f"#{index}"
        try:
            question = RagQuestion.model_validate(raw)
        except ValidationError as exc:
            # Catch-all - normalise vers ValueError en citant l'id fautif
            raise ValueError(f"Question {label} : {_format_error(exc)}") from exc
        if question.id in seen:
            raise ValueError(f"Question {question.id} : id dupliqué")
        seen.add(question.id)
        _check_doc_ids(question, valid_doc_ids)
        questions.append(question)
    return questions


def _check_doc_ids(question: RagQuestion, valid_doc_ids: set[str]) -> None:
    """Vérifie que chaque doc_id référencé existe dans le corpus."""

    refs: list[str] = [*question.sources_attendues, *(question.contexte_isole or [])]
    inconnus = sorted(set(refs) - valid_doc_ids)
    if inconnus:
        raise ValueError(f"Question {question.id} : doc_id inconnu(s) {inconnus}")
