"""Extraction et normalisation déterministes des quantités (valeur, unité), sans LLM."""

import re
import unicodedata
from decimal import Decimal
from typing import NamedTuple


class Quantity(NamedTuple):
    """Nombre normalisé et son unité canonique ('' si absente)."""

    value: Decimal
    unit: str


_UNITS = {
    "%": "%",
    "€": "eur",
    "euro": "eur",
    "euros": "eur",
    "eur": "eur",
    "j": "jours",
    "jour": "jours",
    "jours": "jours",
    "mois": "mois",
    "an": "ans",
    "ans": "ans",
    "annee": "ans",
    "annees": "ans",
}

_WORDS = {
    "zero": 0, "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6,
    "sept": 7, "huit": 8, "neuf": 9, "dix": 10, "onze": 11, "douze": 12, "treize": 13,
    "quatorze": 14, "quinze": 15, "seize": 16, "vingt": 20, "vingts": 20, "trente": 30,
    "quarante": 40, "cinquante": 50, "soixante": 60, "cent": 100, "cents": 100, "mille": 1000,
}  # fmt: skip

_WORD_ALT = "|".join(sorted(_WORDS, key=len, reverse=True))
_WORD_RUN = re.compile(rf"(?<![a-z])(?:{_WORD_ALT}|et)(?:[ -](?:{_WORD_ALT}|et))*(?![a-z])")
_NUM = r"\d{1,3}(?:[ .]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?"
_UNIT_ALT = "|".join(sorted((re.escape(u) for u in _UNITS), key=len, reverse=True))
_QUANTITY = re.compile(rf"(?<![\d.,])({_NUM})(?:\s*({_UNIT_ALT})(?![a-z]))?")


def _words_to_value(tokens: list[str]) -> int | None:
    """Évalue une suite de mots-nombres français, None si elle ne contient aucun nombre."""

    total = current = 0
    previous = ""
    seen = False
    for token in tokens:
        if token == "et":
            continue
        seen = True
        if token in ("cent", "cents"):
            current = (current or 1) * 100
        elif token == "mille":
            total += (current or 1) * 1000
            current = 0
        elif token in ("vingt", "vingts") and previous == "quatre":
            # quatre-vingt(s) est multiplicatif, pas additif
            current += 76
        else:
            current += _WORDS[token]
        previous = token
    return total + current if seen else None


def _replace_word_run(match: re.Match[str]) -> str:
    """Remplace une suite de mots-nombres par ses chiffres, la laisse intacte sinon."""

    tokens = re.split(r"[ -]", match.group(0))
    value = _words_to_value(tokens)
    return match.group(0) if value is None else str(value)


def normaliser(text: str) -> str:
    """Minuscule, sans accents, espaces unifiés, nombres en lettres convertis en chiffres."""

    decomposed = unicodedata.normalize("NFKD", text.lower())
    plain = "".join(c for c in decomposed if not unicodedata.combining(c))
    plain = re.sub(r"[   ]", " ", plain)
    plain = _WORD_RUN.sub(_replace_word_run, plain)
    return re.sub(r"\s+", " ", plain).strip()


def _to_decimal(raw: str) -> Decimal:
    """Convertit un nombre au format français (espace/point milliers, virgule décimale)."""

    if re.fullmatch(r"\d{1,3}(?:[ .]\d{3})+(?:,\d+)?", raw):
        raw = re.sub(r"[ .]", "", raw)
    return Decimal(raw.replace(",", "."))


def _scan(normalized: str) -> list[tuple[Quantity, tuple[int, int]]]:
    """Quantités d'un texte déjà normalisé, avec leur position."""

    found = []
    for match in _QUANTITY.finditer(normalized):
        unit = _UNITS[match.group(2)] if match.group(2) else ""
        found.append((Quantity(_to_decimal(match.group(1)), unit), match.span()))
    return found


def extract_quantities(text: str) -> list[Quantity]:
    """Extrait les quantités (valeur, unité) d'un texte libre."""

    return [quantity for quantity, _ in _scan(normaliser(text))]


def forme_presente(forme: str, text: str) -> bool:
    """Indique si une forme acceptable est présente dans un texte.

    Une forme purement chiffrée (« 60 jours ») est comparée par valeur et unité ; toute autre
    forme est comparée comme sous-chaîne normalisée.
    """

    forme_norm = normaliser(forme)
    text_norm = normaliser(text)
    scanned = _scan(forme_norm)
    residu = forme_norm
    for _, (start, end) in reversed(scanned):
        residu = residu[:start] + residu[end:]
    if scanned and not re.search(r"[a-z]", residu):
        disponibles = [q for q, _ in _scan(text_norm)]
        return all(
            any(d.value == q.value and (not q.unit or d.unit == q.unit) for d in disponibles)
            for q, _ in scanned
        )
    return forme_norm in text_norm
