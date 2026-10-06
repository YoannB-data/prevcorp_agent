"""Tests du schéma des questions d'éval RAG."""

from pathlib import Path

import pytest
import yaml

from src.rag.eval_schema import load_questions

ROOT = Path(__file__).resolve().parent.parent
VALID = {
    "REGLEMENT_prevcorp",
    "RESUME_C87656",
    "NOTICE_CCN_metallurgie",
    "NOTICE_CCN_metallurgie_distracteur",
}


def _q(**overrides):
    """Construit une question valide de type fait_simple, avec surcharges."""

    base = {
        "id": "RC01",
        "question": "Quelle franchise ?",
        "type": "fait_simple",
        "contrat_cible": "C87656",
        "reponse_attendue": "90 jours",
        "sources_attendues": ["RESUME_C87656"],
        "corpus_a_contenir": "franchise ITT",
    }
    base.update(overrides)
    return base


def _load(tmp_path, *questions):
    """Écrit les questions en YAML et les charge."""

    path = tmp_path / "q.yml"
    path.write_text(yaml.safe_dump({"questions": list(questions)}), encoding="utf-8")
    return load_questions(path, VALID)


def test_fichier_valide(tmp_path):
    result = _load(
        tmp_path,
        _q(),
        _q(id="RC02", type="chiffre_precis"),
        _q(id="RC03", type="croisement", sources_attendues=["REGLEMENT_prevcorp", "RESUME_C87656"]),
        _q(id="RC04", type="sans_reponse", sources_attendues=[], contexte_isole=["RESUME_C87656"]),
    )
    assert [q.id for q in result] == ["RC01", "RC02", "RC03", "RC04"]


def test_regle1_sans_reponse_avec_sources(tmp_path):
    q = _q(type="sans_reponse", contexte_isole=["RESUME_C87656"])
    with pytest.raises(ValueError, match="RC01.*sources_attendues vide"):
        _load(tmp_path, q)


def test_regle1_sans_reponse_sans_contexte(tmp_path):
    q = _q(type="sans_reponse", sources_attendues=[])
    with pytest.raises(ValueError, match="RC01.*contexte_isole non vide"):
        _load(tmp_path, q)


def test_contexte_isole_vide_interdit(tmp_path):
    with pytest.raises(ValueError, match="RC01.*contexte_isole présent mais vide"):
        _load(tmp_path, _q(contexte_isole=[]))


def test_regle2_croisement_une_source(tmp_path):
    q = _q(type="croisement", sources_attendues=["RESUME_C87656", "RESUME_C87656"])
    with pytest.raises(ValueError, match="RC01.*2 sources distinctes"):
        _load(tmp_path, q)


@pytest.mark.parametrize("type_", ["fait_simple", "chiffre_precis"])
def test_regle3_sans_source(tmp_path, type_):
    with pytest.raises(ValueError, match="RC01.*au moins 1 source"):
        _load(tmp_path, _q(type=type_, sources_attendues=[]))


def test_regle4_distracteur_en_source(tmp_path):
    q = _q(sources_attendues=["NOTICE_CCN_metallurgie_distracteur"])
    with pytest.raises(ValueError, match="RC01.*distracteur"):
        _load(tmp_path, q)


def test_regle4_distracteur_en_contexte(tmp_path):
    q = _q(contexte_isole=["NOTICE_CCN_metallurgie_distracteur"])
    with pytest.raises(ValueError, match="RC01.*distracteur"):
        _load(tmp_path, q)


def test_regle5_doublon_source(tmp_path):
    q = _q(sources_attendues=["RESUME_C87656", "RESUME_C87656"])
    with pytest.raises(ValueError, match="RC01.*doublons"):
        _load(tmp_path, q)


def test_regle6_ids_dupliques(tmp_path):
    with pytest.raises(ValueError, match="RC01.*id dupliqué"):
        _load(tmp_path, _q(), _q())


@pytest.mark.parametrize("champ", ["sources_attendues", "contexte_isole"])
def test_regle7_doc_id_inconnu(tmp_path, champ):
    q = _q(**{champ: ["RESUME_C00000"]})
    with pytest.raises(ValueError, match="RC01.*RESUME_C00000"):
        _load(tmp_path, q)


def test_cle_inconnue_interdite(tmp_path):
    with pytest.raises(ValueError, match="RC01"):
        _load(tmp_path, _q(extra="x"))


def test_id_mal_forme(tmp_path):
    with pytest.raises(ValueError, match="Question XX1"):
        _load(tmp_path, _q(id="XX1"))


def test_texte_vide(tmp_path):
    with pytest.raises(ValueError, match="RC01.*question"):
        _load(tmp_path, _q(question="  "))


def test_message_cite_l_id_une_seule_fois(tmp_path):
    with pytest.raises(ValueError) as exc:
        _load(tmp_path, _q(sources_attendues=[]))
    assert str(exc.value).count("RC01") == 1


def test_fichier_reel_respecte_le_contrat():
    pdfs = list((ROOT / "corpus").glob("*.pdf"))
    if not pdfs:
        pytest.skip("corpus/ absent ou vide (gitignoré)")
    valid = {p.stem for p in pdfs}
    questions = load_questions(ROOT / "evals" / "rag_questions_v1_25.yml", valid)
    assert len(questions) == 25


def test_contexte_effectif_defaut_sur_sources(tmp_path):
    (q,) = _load(tmp_path, _q())
    assert q.contexte_effectif == q.sources_attendues == ["RESUME_C87656"]


def test_contexte_effectif_utilise_contexte_isole(tmp_path):
    (q,) = _load(
        tmp_path, _q(type="sans_reponse", sources_attendues=[], contexte_isole=["RESUME_C87656"])
    )
    assert q.contexte_effectif == ["RESUME_C87656"]
