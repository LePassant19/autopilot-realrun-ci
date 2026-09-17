"""Couplage code ↔ workflow : la CI lance exactement `ci_contract.TEST_COMMAND`.

Préexistant sur `main`, exprès : c'est le couplage de harness STORY-066 (`gates.json` rendu depuis le
code), sur un chemin que l'agent ne peut pas écrire (`.github/workflows/**`, protégé)."""
from pathlib import Path

from src import ci_contract

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "autopilot-ci.yml"


def test_the_ci_runs_exactly_the_contract_command():
    assert f"- run: {ci_contract.TEST_COMMAND}\n" in WORKFLOW.read_text(encoding="utf-8")
