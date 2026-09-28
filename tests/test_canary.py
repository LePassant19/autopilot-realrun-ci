"""Canari STORY-009 : preuves exécutables d'AC1..AC3 (aucun skip — l'historique complet est disponible en CI)."""
import datetime
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANARY = ROOT / "CANARY.md"
ALLOWED = {"CANARY.md", "tests/test_canary.py"}
CANARY_LINE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _canary_date() -> datetime.date:
    match = CANARY_LINE.search(CANARY.read_text(encoding="utf-8"))
    assert match, "CANARY.md ne contient aucune ligne `canary YYYY-MM-DD`"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_a_canary_line():
    assert CANARY.is_file(), "CANARY.md doit exister à la racine du dépôt"
    assert CANARY_LINE.search(CANARY.read_text(encoding="utf-8"))


def test_ac2_canary_date_is_todays_utc_date():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    assert _canary_date() == today


def test_ac3_diff_is_limited_to_canary_files():
    try:
        _git("rev-parse", "--verify", "-q", "origin/main")
        base_ref = "origin/main"
    except subprocess.CalledProcessError:
        base_ref = "main"
    merge_base = _git("merge-base", "HEAD", base_ref)
    assert merge_base, f"merge-base de HEAD avec {base_ref} introuvable"
    changed = set(_git("diff", "--name-only", merge_base).splitlines())
    assert changed <= ALLOWED, f"fichiers hors périmètre : {sorted(changed - ALLOWED)}"
