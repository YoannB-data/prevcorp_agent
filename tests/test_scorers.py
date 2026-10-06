"""Tests des scorers : extraction numérique déterministe et points obligatoires/interdits."""

from decimal import Decimal

import pytest

from src.rag.eval_schema import RagQuestion
from src.rag.evaluation.models import Answer
from src.rag.evaluation.numbers import Quantity, extract_quantities, forme_presente
from src.rag.evaluation.scorers import score


def _question(obligatoires, interdits=(), type_="chiffre_precis"):
    """Construit une question scorable avec des points déterministes."""

    def pts(prefix, formes_list):
        return [
            {"id": f"{prefix}{i}", "texte": f[0], "formes": f, "verif": "deterministe"}
            for i, f in enumerate(formes_list)
        ]

    return RagQuestion.model_validate(
        {
            "id": "RC01",
            "question": "Quelle franchise ?",
            "type": type_,
            "contrat_cible": None,
            "reponse_attendue": "60 jours",
            "sources_attendues": ["RESUME_C39949"],
            "corpus_a_contenir": "franchise",
            "points_obligatoires": pts("O", obligatoires),
            "points_interdits": pts("I", interdits),
        }
    )


@pytest.mark.parametrize(
    "texte",
    [
        "La franchise est de 60 jours.",
        "La franchise est de soixante jours.",
        "La franchise est de 60 j.",
        "La franchise est de 60,0 jours.",
        "La franchise est de 60 jours.",
        "La franchise est de 60jours.",
    ],
)
def test_chiffre_precis_variantes_de_format(texte):
    q = _question([["60 jours"]])
    assert score(q, Answer(texte)).passed


def test_piege_60_contre_90():
    q = _question([["60 jours"]], interdits=[["90 jours"]])
    assert score(q, Answer("La franchise est de 60 jours.")).passed
    assert not score(q, Answer("La franchise est de 90 jours.")).passed
    resultat = score(q, Answer("La franchise est de 90 jours."))
    assert resultat.details == {"O0": False, "I0": False}


def test_point_interdit_declenche_meme_avec_le_bon_chiffre():
    q = _question([["60 jours"]], interdits=[["90 jours"]])
    assert not score(q, Answer("60 jours, et non 90 jours.")).passed


def test_une_forme_suffit_parmi_les_formes_acceptables():
    q = _question([["3 mois", "90 jours"]])
    assert score(q, Answer("Un délai de trois mois.")).passed
    assert score(q, Answer("Un délai de 90 jours.")).passed
    assert not score(q, Answer("Un délai de 6 mois.")).passed


def test_aucun_point_obligatoire_leve():
    q = _question([])
    with pytest.raises(ValueError, match="non scorable"):
        score(q, Answer("60 jours"))


def test_point_juge_non_branche_dans_le_scorer_deterministe():
    q = RagQuestion.model_validate(
        {
            "id": "RC02",
            "question": "q",
            "type": "fait_simple",
            "contrat_cible": None,
            "reponse_attendue": "r",
            "sources_attendues": ["FAQ_prevcorp"],
            "corpus_a_contenir": "c",
            "points_obligatoires": [{"id": "O0", "texte": "t", "formes": ["f"], "verif": "juge"}],
        }
    )
    with pytest.raises(NotImplementedError):
        score(q, Answer("f"))


def test_chiffre_precis_refuse_le_juge():
    with pytest.raises(ValueError, match="chiffre_precis interdit"):
        RagQuestion.model_validate(
            {
                "id": "RC03",
                "question": "q",
                "type": "chiffre_precis",
                "contrat_cible": None,
                "reponse_attendue": "r",
                "sources_attendues": ["FAQ_prevcorp"],
                "corpus_a_contenir": "c",
                "points_obligatoires": [
                    {"id": "O0", "texte": "t", "formes": ["f"], "verif": "juge"}
                ],
            }
        )


@pytest.mark.parametrize(
    ("texte", "attendu"),
    [
        ("1 900 €", [Quantity(Decimal(1900), "eur")]),
        ("1 900 euros", [Quantity(Decimal(1900), "eur")]),
        ("1.900 €", [Quantity(Decimal(1900), "eur")]),
        ("5,5 %", [Quantity(Decimal("5.5"), "%")]),
        ("quatre-vingt-dix jours", [Quantity(Decimal(90), "jours")]),
        ("quatre-vingts jours", [Quantity(Decimal(80), "jours")]),
        ("soixante-quinze %", [Quantity(Decimal(75), "%")]),
        ("deux cents euros", [Quantity(Decimal(200), "eur")]),
        ("mille cinq cents €", [Quantity(Decimal(1500), "eur")]),
        ("de 12 à 17 ans", [Quantity(Decimal(12), ""), Quantity(Decimal(17), "ans")]),
    ],
)
def test_extract_quantities(texte, attendu):
    assert extract_quantities(texte) == attendu


def test_forme_non_chiffree_comparee_en_sous_chaine():
    assert forme_presente("attestation de vie commune", "Une Attestation de vie commune.")
    assert not forme_presente("attestation de vie commune", "un justificatif de domicile")


def test_forme_chiffree_sans_unite_accepte_toute_unite():
    assert forme_presente("90", "délai de 90 jours")
    assert not forme_presente("90 jours", "délai de 90 mois")
