"""Preuve exécutable d'AC1..AC3 de STORY-009 (canari)."""
import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"

ALLOWED_CHANGED_FILES = {"CANARY.md", "tests/test_canary.py"}


def _run_git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_ac2_canary_date_matches_today():
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\d{4}-\d{2}-\d{2})$", content, re.MULTILINE)
    assert match, f"aucune ligne 'canary <date>' trouvée dans {CANARY_PATH}"

    canary_date = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc


def test_ac3_only_canary_files_changed():
    base_ref = "main"
    try:
        _run_git("rev-parse", "--verify", "origin/main")
        base_ref = "origin/main"
    except subprocess.CalledProcessError:
        pass

    merge_base = _run_git("merge-base", "HEAD", base_ref)
    changed = _run_git("diff", "--name-only", merge_base).splitlines()

    assert set(changed) <= ALLOWED_CHANGED_FILES, changed
