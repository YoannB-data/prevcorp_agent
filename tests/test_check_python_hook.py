"""Tests du hook PostToolUse .claude/hooks/check_python.py."""

import importlib.util
import json
from pathlib import Path

import pytest

_HOOK_PATH = Path(__file__).parent.parent / ".claude" / "hooks" / "check_python.py"
_spec = importlib.util.spec_from_file_location("check_python", _HOOK_PATH)
assert _spec is not None and _spec.loader is not None
check_python = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_python)


def _payload(path: Path) -> str:
    """Construit le JSON stdin d'un hook PostToolUse."""

    return json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(path)}})


def test_clean_py_returns_0(tmp_path: Path) -> None:
    """Un .py propre sort en 0."""

    f = tmp_path / "ok.py"
    f.write_text("x = 1\n")
    assert check_python.main(_payload(f)) == 0


def test_faulty_py_returns_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Un .py fautif (import inutilisé) sort en 2 avec la sortie de ruff sur stderr."""

    f = tmp_path / "bad.py"
    f.write_text("import os\n")
    assert check_python.main(_payload(f)) == 2
    assert "F401" in capsys.readouterr().err


def test_md_returns_0(tmp_path: Path) -> None:
    """Un fichier non-.py est ignoré."""

    f = tmp_path / "notes.md"
    f.write_text("import os\n")
    assert check_python.main(_payload(f)) == 0


def test_mypy_runs_only_on_src(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Une erreur de type est détectée sous /src/ mais pas ailleurs."""

    code = "def f(x: int) -> str:\n    return x\n"
    outside = tmp_path / "other" / "t.py"
    inside = tmp_path / "src" / "t.py"
    for f in (outside, inside):
        f.parent.mkdir()
        f.write_text(code)
    assert check_python.main(_payload(outside)) == 0
    assert check_python.main(_payload(inside)) == 2
    assert "[mypy]" in capsys.readouterr().err


def test_missing_tool_returns_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Un outil introuvable donne un message explicite et exit 2."""

    monkeypatch.setattr(check_python.shutil, "which", lambda _tool: None)
    f = tmp_path / "ok.py"
    f.write_text("x = 1\n")
    assert check_python.main(_payload(f)) == 2
    assert "introuvable" in capsys.readouterr().err
