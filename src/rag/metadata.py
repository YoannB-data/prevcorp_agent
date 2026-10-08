"""Métadonnées des documents du corpus RAG (sans client externe, importable en test)."""

import re
from dataclasses import dataclass

DOC_TYPE_BY_PREFIX = {
    "REGLEMENT_": "reglement",
    "NOTICE_": "notice_ccn",
    "RESUME_": "resume_contrat",
    "FAQ_": "faq",
}


def doc_type_from_filename(filename: str) -> str:
    """Infère le type de document depuis le préfixe du nom de fichier."""

    name = filename.upper()
    for prefix, doc_type in DOC_TYPE_BY_PREFIX.items():
        if name.startswith(prefix):
            return doc_type
    return "autre"


DOC_TYPE_LABELS = {
    "reglement": "règlement",
    "notice_ccn": "notice CCN",
    "resume_contrat": "résumé des garanties",
    "faq": "FAQ",
    "autre": "document",
}

BANNER = "PREVCORP PRÉVOYANCE"
_DASH = r"[—–-]"
_CONTRACT_RE = re.compile(r"Contrat\s+n\S*\s*(C\d{5})")
_CCN_RE = re.compile(r"^Convention collective nationale(.*)$", re.MULTILINE)
_CCN_ARTICLE_RE = re.compile(rf"^\s*(?:{_DASH}\s*)?(?:du |de la |de l'|des |de )?", re.IGNORECASE)


class PrefixConstructionError(ValueError):
    """Le préfixe de contexte d'un document ne peut pas être construit."""


@dataclass(frozen=True)
class ContractInfo:
    """Identité d'un contrat lue dans son résumé des garanties."""

    contract_id: str
    ccn: str
    category: str


def extract_title(text: str, filename: str) -> str:
    """Titre = lignes en majuscules qui suivent la bannière de page (la bannière est commune)."""

    lines = [line.strip() for line in text.splitlines()]
    banners = [i for i, line in enumerate(lines) if line.upper() == BANNER]
    if not banners:
        raise PrefixConstructionError(f"titre introuvable dans {filename} (bannière absente)")
    title_lines = []
    for line in lines[banners[0] + 1 :]:
        if not line.isupper():
            break
        title_lines.append(line)
    if not title_lines:
        raise PrefixConstructionError(
            f"titre introuvable dans {filename} (aucune ligne en majuscules après la bannière)"
        )
    return " ".join(title_lines)


def extract_contract_info(text: str, filename: str) -> ContractInfo:
    """Lit l'identifiant, la CCN et la catégorie dans le sous-titre d'un résumé des garanties."""

    contract = _CONTRACT_RE.search(text)
    if contract is None:
        raise PrefixConstructionError(
            f"contrat introuvable dans {filename} (ligne « Contrat n° » absente)"
        )
    ccn_line = _CCN_RE.search(text)
    if ccn_line is None:
        raise PrefixConstructionError(
            f"CCN introuvable dans {filename} (ligne « Convention collective nationale » absente)"
        )
    parts = re.split(rf"\s+{_DASH}\s+", ccn_line.group(1).strip())
    if len(parts) < 2 or not parts[-1].strip():
        raise PrefixConstructionError(
            f"catégorie introuvable dans {filename} (« {ccn_line.group(0)} »)"
        )
    ccn = _CCN_ARTICLE_RE.sub("", " — ".join(parts[:-1]), count=1).strip(" —–-")
    if not ccn:
        raise PrefixConstructionError(f"CCN vide dans {filename} (« {ccn_line.group(0)} »)")
    return ContractInfo(contract_id=contract.group(1), ccn=ccn, category=parts[-1].strip())


def build_context_prefix(title: str, doc_type: str, contract: ContractInfo | None) -> str:
    """Construit le préfixe de contexte sans doc_id (le nom de fichier peut trahir le rôle)."""

    if contract is not None:
        return (
            f"[{contract.contract_id} | {DOC_TYPE_LABELS['resume_contrat']} | "
            f"Contrat {contract.contract_id} — {contract.ccn}, {contract.category}]"
        )
    return f"[{title} | {DOC_TYPE_LABELS.get(doc_type, DOC_TYPE_LABELS['autre'])}]"
