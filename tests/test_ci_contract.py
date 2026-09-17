"""Couplage code ↔ workflow : la CI lance exactement `ci_contract.TEST_COMMAND`.

Préexistant sur `main`, exprès : c'est le couplage de harness STORY-066 (`gates.json` rendu depuis le
code), sur un chemin que l'agent ne peut pas écrire (`.github/workflows/**`, protégé)."""
import inspect
from pathlib import Path

from src import ci_contract

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "autopilot-ci.yml"


def test_the_ci_runs_exactly_the_contract_command():
    assert f"- run: {ci_contract.TEST_COMMAND}\n" in WORKFLOW.read_text(encoding="utf-8")


def test_ac1_test_command_is_quiet():
    assert ci_contract.TEST_COMMAND == "uv run --with pytest pytest -q"


def test_ac2_workflow_declares_quiet_run_and_keeps_the_rest():
    # Rouge tant que la proposition sur le chemin protégé n'est pas appliquée
    # (STORY-011 : `.github/workflows/**` n'est jamais écrit par l'agent) — vert
    # une fois `.github/workflows/autopilot-ci.yml` mis à jour avec `TEST_COMMAND`.
    content = WORKFLOW.read_text(encoding="utf-8")
    assert f"- run: {ci_contract.TEST_COMMAND}\n" in content
    assert "fetch-depth: 0" in content
    assert "- run: uv sync --all-extras --dev\n" in content


def test_ac3_coupling_test_not_removed_weakened_or_skipped():
    assert not getattr(test_the_ci_runs_exactly_the_contract_command, "pytestmark", None)
    assert inspect.getsource(test_the_ci_runs_exactly_the_contract_command) == (
        "def test_the_ci_runs_exactly_the_contract_command():\n"
        '    assert f"- run: {ci_contract.TEST_COMMAND}\\n" in WORKFLOW.read_text(encoding="utf-8")\n'
    )
