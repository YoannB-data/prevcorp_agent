"""Tests de la configuration des modèles par rôle et de la table de tarifs."""

import pytest

from src import config


def test_roles_restent_sur_sonnet_46():
    """Le découplage par rôle ne change aucun modèle."""

    assert config.AGENT_MODEL == "claude-sonnet-4-6"
    assert config.ROUTER_MODEL == "claude-sonnet-4-6"
    assert config.JUDGE_MODEL == "claude-sonnet-4-6"


def test_cout_sonnet_46_identique_a_l_ancien_tarif_unique():
    """3 $ / 15 $ par M tokens, comme l'ancien couple COST_PER_*_TOKEN."""

    cost = config.compute_cost("claude-sonnet-4-6", 6292, 284)
    assert cost == pytest.approx(6292 * 3.0 / 1_000_000 + 284 * 15.0 / 1_000_000)


def test_modele_sans_tarif_leve_keyerror():
    """Pas de tarif par défaut silencieux."""

    with pytest.raises(KeyError):
        config.compute_cost("claude-inconnu", 1, 1)


def test_tous_les_roles_ont_un_tarif():
    """Un changement de rôle ne doit pas casser le calcul de coût."""

    for model in (config.AGENT_MODEL, config.ROUTER_MODEL, config.JUDGE_MODEL):
        assert model in config.MODEL_PRICES
