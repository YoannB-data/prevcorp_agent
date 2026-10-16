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


def test_validation_leve_valueerror_nommant_le_role_sans_tarif():
    """Le démarrage échoue avec le rôle et le modèle fautifs."""

    with pytest.raises(ValueError, match=r"JUDGE_MODEL='claude-inconnu'"):
        config._validate_models(
            {"AGENT_MODEL": "claude-sonnet-4-6", "JUDGE_MODEL": "claude-inconnu"},
            config.MODEL_PRICES,
            config.MODEL_PARAMS,
        )


def test_validation_passe_quand_tous_les_roles_ont_un_tarif():
    """Aucune erreur si la table couvre tous les rôles."""

    config._validate_models(
        {"AGENT_MODEL": "claude-sonnet-5-5"}, config.MODEL_PRICES, config.MODEL_PARAMS
    )


def test_validation_leve_valueerror_si_modele_sans_parametres():
    """Un modèle tarifé mais absent de MODEL_PARAMS fait échouer le démarrage."""

    prices = {**config.MODEL_PRICES, "claude-sans-params": (1.0, 2.0)}
    with pytest.raises(ValueError, match=r"MODEL_PARAMS : ROUTER_MODEL='claude-sans-params'"):
        config._validate_models({"ROUTER_MODEL": "claude-sans-params"}, prices, config.MODEL_PARAMS)


def test_sampling_kwargs_modele_avec_temperature():
    """Sonnet 4.6 reçoit temperature."""

    assert config.sampling_kwargs("claude-sonnet-4-6", 0) == {"temperature": 0}


def test_sampling_kwargs_modele_sans_temperature():
    """Sonnet 5.5 n'en reçoit aucun (non défaut = 400)."""

    assert config.sampling_kwargs("claude-sonnet-5-5", 0) == {}


def test_sampling_kwargs_modele_inconnu_leve_valueerror():
    """Pas de défaut silencieux pour un modèle hors table."""

    with pytest.raises(ValueError, match="MODEL_PARAMS"):
        config.sampling_kwargs("claude-inconnu", 0)


def test_juge_garde_temperature_0_sur_46():
    """Le juge sur 4.6 envoie temperature=0 ; construit à l'init, donc échoue tôt si inconnu."""

    from src.rag.evaluation.judge import AnthropicJudge

    judge = AnthropicJudge(None, config.JUDGE_MODEL)  # type: ignore[arg-type]
    assert judge.sampling == {"temperature": 0}
    with pytest.raises(ValueError):
        AnthropicJudge(None, "claude-inconnu")  # type: ignore[arg-type]


def test_agent_call_kwargs_55_default_sans_champ_thinking(monkeypatch):
    """5.5 en mode default : max_tokens 4096, ni thinking ni temperature."""

    monkeypatch.setattr(config, "AGENT_MODEL", "claude-sonnet-5-5")
    assert config.agent_call_kwargs(temperature=0) == {"max_tokens": 4096}


def test_agent_call_kwargs_between_tools(monkeypatch):
    """La variante between_tools ajoute le champ thinking, sans toucher au code."""

    monkeypatch.setattr(config, "AGENT_MODEL", "claude-sonnet-5-5")
    monkeypatch.setattr(config, "AGENT_THINKING_MODE", "between_tools")
    assert config.agent_call_kwargs(temperature=0) == {
        "max_tokens": 4096,
        "thinking": {"type": "between_tools"},
    }


def test_agent_call_kwargs_modele_avec_temperature(monkeypatch):
    """Sur 4.6, temperature est transmise et max_tokens reste à 1024."""

    monkeypatch.setattr(config, "AGENT_MODEL", "claude-sonnet-4-6")
    assert config.agent_call_kwargs(temperature=0) == {"max_tokens": 1024, "temperature": 0}
    assert config.agent_call_kwargs() == {"max_tokens": 1024}


def test_mode_thinking_inconnu_leve_au_demarrage(monkeypatch):
    """Un AGENT_THINKING_MODE invalide fait échouer l'import de config."""

    import importlib

    monkeypatch.setenv("AGENT_THINKING_MODE", "nimporte")
    with pytest.raises(ValueError, match="AGENT_THINKING_MODE"):
        importlib.reload(config)
    monkeypatch.delenv("AGENT_THINKING_MODE")
    importlib.reload(config)
