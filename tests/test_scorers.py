"""Tests des scorers : extraction numérique déterministe et points obligatoires/interdits."""

from decimal import Decimal

import pytest

from src.rag.eval_schema import Point, RagQuestion
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
    q = _question([["60 jours"]])
    # le schéma l'interdit : on contourne la validation pour tester la garde du scorer
    q.points_obligatoires = []
    with pytest.raises(ValueError, match="non scorable"):
        score(q, Answer("60 jours"))


class FakeJudge:
    """Juge factice : verdicts prédéfinis par id, appels mémorisés."""

    def __init__(self, verdicts):
        self.verdicts = verdicts
        self.appels = []

    def evaluate(self, question, answer_text, points):
        self.appels.append([p.id for p in points])
        return {p.id: self.verdicts[p.id] for p in points}


def _question_ecart():
    """Question « écart » : le rattachement valeur ↔ document est jugé, pas extrait."""

    def pt(pid, texte, formes):
        return {"id": pid, "texte": texte, "formes": formes, "verif": "juge"}

    return RagQuestion.model_validate(
        {
            "id": "RC05",
            "question": "Y a-t-il un écart sur la franchise ITT ?",
            "type": "croisement",
            "contrat_cible": "C39949",
            "reponse_attendue": "Résumé 60 jours, Notice 90 jours",
            "sources_attendues": ["RESUME_C39949", "NOTICE_CCN_agriculture"],
            "corpus_a_contenir": "écart",
            "points_obligatoires": [
                pt("O0", "Le Résumé C39949 indique 60 jours", ["60 jours"]),
                pt("O1", "La Notice Agriculture indique 90 jours", ["90 jours"]),
            ],
        }
    )


def test_valeurs_inversees_envoyees_au_juge():
    # Une présence de paires accepterait cette réponse : seul le juge voit l'inversion
    inversee = Answer("Le Résumé indique 90 jours, la Notice indique 60 jours.")
    assert forme_presente("60 jours", inversee.text) and forme_presente("90 jours", inversee.text)
    juge = FakeJudge({"O0": False, "O1": False})
    resultat = score(_question_ecart(), inversee, juge)
    assert not resultat.passed
    assert resultat.needs_review
    assert juge.appels == [["O0", "O1"]]


def test_valeurs_correctes_validees_par_le_juge():
    juge = FakeJudge({"O0": True, "O1": True})
    resultat = score(_question_ecart(), Answer("Résumé 60 jours, Notice 90 jours."), juge)
    assert resultat.passed and resultat.needs_review


def test_point_juge_sans_juge_leve():
    with pytest.raises(ValueError, match="sans juge"):
        score(_question_ecart(), Answer("x"))


def test_points_mixtes_un_seul_appel_au_juge_pour_les_points_juges():
    q = _question_ecart()
    q.points_interdits.append(
        Point(id="X0", texte="Parents", formes=["parents"], verif="deterministe")
    )
    juge = FakeJudge({"O0": True, "O1": True})
    resultat = score(q, Answer("60 jours / 90 jours, pas de parents."), juge)
    assert juge.appels == [["O0", "O1"]]
    # le déterministe ne comprend pas la négation : c'est la limite documentée des points interdits
    assert not resultat.passed
    assert resultat.details["X0"] is False


def test_sans_point_juge_pas_de_relecture():
    q = _question([["60 jours"]])
    assert not score(q, Answer("60 jours")).needs_review


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
