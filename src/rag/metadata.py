"""Métadonnées des documents du corpus RAG (sans client externe, importable en test)."""

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
