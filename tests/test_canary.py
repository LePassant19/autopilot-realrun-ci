"""Canari STORY-009 : preuve exécutable qu'un CANARY.md à jour existe et que rien d'autre n'a bougé."""
import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
ALLOWED_CHANGED_FILES = {"CANARY.md", "tests/test_canary.py"}


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"canary (\S+)", content)
    assert match, f"aucune ligne 'canary <date>' trouvée dans {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def _today_utc() -> datetime.date:
    return datetime.datetime.now(datetime.timezone.utc).date()


def test_ac1_canary_file_exists_with_today_utc_date():
    assert CANARY_PATH.is_file()
    assert _read_canary_date() == _today_utc()


def test_ac2_canary_date_parses_and_matches_utc_today():
    assert _read_canary_date() == _today_utc()


def _merge_base_ref() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return "origin/main" if result.returncode == 0 else "main"


def test_ac3_only_canary_files_changed():
    ref = _merge_base_ref()
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", ref],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    diff = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    changed = {line for line in diff if line}
    assert changed <= ALLOWED_CHANGED_FILES, changed
