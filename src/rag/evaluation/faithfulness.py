"""Faithfulness maison : part des affirmations de la réponse appuyées par les chunks récupérés."""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import anthropic

from src.rag.evaluation.judge import AnthropicJudge, parse_verdicts
from src.rag.evaluation.models import RetrievedChunk
from src.rag.evaluation.report import TYPES

FAITHFULNESS_MAX_TOKENS = 1024
CLAIM_ID_PREFIX = "A"

EXTRACT_SYSTEM_PROMPT = """Tu extrais les affirmations factuelles d'une réponse.
Règles :
- Une affirmation = une proposition atomique et autonome (un fait, un chiffre, une condition).
- Reformule sans pronom ni renvoi au contexte pour que chaque affirmation se comprenne seule.
- Ignore les citations de sources et les formules de politesse.
- Une réponse peut mélanger refus et faits : extrais les faits énoncés, ignore seulement la \
phrase de refus (« je ne trouve pas cette information »).
- Ignore les affirmations sur les documents consultés ou disponibles (« le Règlement n'a pas été \
consulté », « les extraits ne précisent pas »).
- Ignore les jugements de valeur et les recommandations (« plus favorable », « conseillé »), \
mais garde les valeurs chiffrées comparées.
- Renvoie une liste vide uniquement si la réponse n'énonce aucun fait.
Réponds uniquement par un tableau JSON de chaînes, sans commentaire."""

VERIFY_SYSTEM_PROMPT = """Tu es un correcteur strict. On te donne des extraits de documents et \
une liste d'affirmations numérotées par identifiant.
Pour CHAQUE affirmation, réponds true si les extraits la SOUTIENNENT explicitement, false sinon.
Règles :
- Tu n'utilises aucune connaissance extérieure aux extraits.
- Une affirmation que les extraits contredisent, ou dont ils ne parlent pas, est false.
- Ne note rien d'autre : pas de commentaire, pas de score.
Réponds uniquement par un objet JSON {"<id>": true|false, ...} couvrant tous les identifiants."""


@dataclass(frozen=True)
class FaithfulnessResult:
    """Affirmations d'une réponse et leur verdict d'appui ; le score est None sans affirmation."""

    claims: dict[str, str]
    verdicts: dict[str, bool]

    @property
    def score(self) -> float | None:
        """Affirmations appuyées / total, None si la réponse n'affirme rien."""

        if not self.claims:
            return None
        return sum(self.verdicts.values()) / len(self.claims)

    @property
    def unsupported(self) -> list[str]:
        """Textes des affirmations non appuyées par les chunks."""

        return [text for cid, text in self.claims.items() if not self.verdicts[cid]]


@dataclass
class FaithfulnessRow:
    """Résultat d'une question : score, affirmations non appuyées, ou erreur d'I/O."""

    id: str
    type: str
    score: float | None = None
    n_claims: int = 0
    unsupported: list[str] = field(default_factory=list)
    answer: str = ""
    error: str | None = None


def parse_claims(raw: str) -> list[str]:
    """Extrait le tableau JSON d'affirmations de la sortie du juge, en exigeant des chaînes."""

    # tolère un éventuel fence ```json autour du tableau
    match = re.search(r"\[.*\]", raw, flags=re.DOTALL)
    if match is None:
        raise ValueError(f"sortie du juge sans tableau JSON : {raw!r}")
    data = json.loads(match.group(0))
    if not all(isinstance(c, str) and c.strip() for c in data):
        raise ValueError(f"affirmations non textuelles : {raw!r}")
    return data


def _ask(judge: AnthropicJudge, system: str, user_message: str) -> str:
    """Un appel du juge à temperature=0, retourne le texte brut."""

    response = judge.client.messages.create(
        model=judge.model,
        max_tokens=FAITHFULNESS_MAX_TOKENS,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    block = response.content[0]
    assert isinstance(block, anthropic.types.TextBlock)
    return block.text


def _format_chunks(chunks: list[RetrievedChunk]) -> str:
    """Extraits numérotés avec leur document, tels que le générateur les voit."""

    return "\n\n".join(f"[{i}] ({c.doc_id})\n{c.text}" for i, c in enumerate(chunks, 1))


def score_faithfulness(
    judge: AnthropicJudge, question: str, answer: str, chunks: list[RetrievedChunk]
) -> FaithfulnessResult:
    """Extrait les affirmations de la réponse, puis vérifie chacune contre les chunks."""

    claims_raw = parse_claims(
        _ask(judge, EXTRACT_SYSTEM_PROMPT, f"Question : {question}\n\n{answer}")
    )
    claims = {f"{CLAIM_ID_PREFIX}{i}": text for i, text in enumerate(claims_raw, 1)}
    # Guard - sans affirmation il n'y a rien à vérifier, et pas de second appel
    if not claims:
        return FaithfulnessResult(claims={}, verdicts={})
    listing = "\n".join(f"- {cid} : {text}" for cid, text in claims.items())
    raw = _ask(
        judge,
        VERIFY_SYSTEM_PROMPT,
        f"Extraits :\n{_format_chunks(chunks)}\n\nAffirmations :\n{listing}",
    )
    return FaithfulnessResult(claims=claims, verdicts=parse_verdicts(raw, list(claims)))


def mean_score(rows: list[FaithfulnessRow], type_: str | None = None) -> str:
    """Moyenne des scores (questions sans erreur ni score nul), « N/A » si aucune."""

    scores = [
        r.score
        for r in rows
        if r.error is None and r.score is not None and (type_ is None or r.type == type_)
    ]
    return f"{sum(scores) / len(scores):.2f} ({len(scores)} q.)" if scores else "N/A"


def render_row(row: FaithfulnessRow) -> str:
    """Section d'une question : score, affirmations non appuyées, réponse en citation."""

    lines = [f"### {row.id} ({row.type})", ""]
    if row.error is not None:
        lines += [f"- **ERREUR d'I/O** : {row.error}", ""]
        return "\n".join(lines)
    score = "N/A (aucune affirmation)" if row.score is None else f"{row.score:.2f}"
    lines += [f"- faithfulness : {score} ({row.n_claims} affirmations)"]
    if row.unsupported:
        lines += ["- affirmations NON appuyées :", *(f"  - {text}" for text in row.unsupported)]
    corps = row.answer.strip() or "(aucune)"
    lines += ["", "**Réponse e2e**", "", *(f"> {ligne}" for ligne in corps.splitlines()), ""]
    return "\n".join(lines)


def render_report(
    rows: list[FaithfulnessRow],
    *,
    date: datetime,
    yaml_hash: str,
    model: str,
    judge_model: str,
    k: int,
    variant: str,
) -> str:
    """Rapport markdown : en-tête, moyennes par type, détail par question."""

    erreurs = sum(r.error is not None for r in rows)
    lines = [
        "# Rapport faithfulness (juge maison)",
        "",
        f"- Date : {date.isoformat(timespec='seconds')}",
        f"- Hash du YAML : {yaml_hash}",
        f"- Modèle : {model}",
        f"- Modèle du juge : {judge_model}",
        "- Temperature : 0.0",
        f"- k : {k}",
        f"- Variante d'ingestion : {variant} (vérifiée contre la collection)",
        "",
        "## Synthèse",
        "",
        f"Questions : {len(rows)} dont {erreurs} en erreur d'I/O (exclues des moyennes).",
        "",
        "| Type | Faithfulness moyenne |",
        "|---|---|",
        f"| **Tous** | {mean_score(rows)} |",
        *(f"| {t} | {mean_score(rows, t)} |" for t in TYPES),
        "",
        "## Détail par question",
        "",
        *(render_row(r) for r in rows),
    ]
    return "\n".join(lines)


def report_filename(date: datetime, variant: str, yaml_hash: str) -> str:
    """Nom de fichier : date + variante d'ingestion + hash du YAML."""

    return f"faithfulness_{date.strftime('%Y%m%d_%H%M%S')}_{variant}_{yaml_hash}.md"


def write_report(content: str, directory: Path, filename: str) -> Path:
    """Écrit le rapport dans le dossier donné."""

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(content, encoding="utf-8")
    return path
