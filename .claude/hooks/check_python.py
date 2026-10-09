"""Hook PostToolUse : ruff sur tout .py écrit, puis mypy si le fichier est dans src/."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _run_tool(tool: str, file_path: str, cwd: str) -> tuple[int, str]:
    """Exécute un outil sur le fichier et renvoie (code retour, sortie combinée)."""

    # Guard - un outil absent ne doit jamais passer pour un fichier propre
    executable = shutil.which(tool)
    if executable is None:
        return 2, f"check_python: '{tool}' introuvable dans le PATH (uv sync --all-groups ?)\n"

    # Config lue dans pyproject.toml via cwd : aucun flag en dur
    args = [executable, "check", file_path] if tool == "ruff" else [executable, file_path]
    result = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout + result.stderr


def main(raw_input: str) -> int:
    """Vérifie le fichier décrit par le JSON du hook et renvoie le code de sortie."""

    payload = json.loads(raw_input)
    file_path = str(payload.get("tool_input", {}).get("file_path", "")).replace("\\", "/")

    # Guard - seuls les .py sont vérifiés
    if not file_path.endswith(".py"):
        return 0

    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or str(Path.cwd())
    tools = ["ruff"]
    # mypy ne couvre que src/ en CI : segment "/src/", pas un préfixe
    if "/src/" in file_path:
        tools.append("mypy")

    failures = []
    for tool in tools:
        code, output = _run_tool(tool, file_path, cwd)
        if code != 0:
            failures.append(f"[{tool}]\n{output}")

    if failures:
        sys.stderr.write("\n".join(failures))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin.read()))
