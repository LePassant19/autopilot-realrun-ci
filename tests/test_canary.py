"""Canari : preuve exécutable qu'AC1 (contenu de CANARY.md) et AC3 (périmètre du diff) tiennent."""
import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
ALLOWED_CHANGED_FILES = {"CANARY.md", "tests/test_canary.py"}


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\S+)$", content, flags=re.MULTILINE)
    assert match, f"pas de ligne 'canary <date>' dans {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_utc_date():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today


def test_ac2_canary_date_parses_and_matches_today():
    parsed = datetime.date.fromisoformat(str(_read_canary_date()))
    today = datetime.datetime.now(datetime.timezone.utc).date()
    assert parsed == today


def _merge_base_ref() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "origin/main"],
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
    assert changed <= ALLOWED_CHANGED_FILES, changed - ALLOWED_CHANGED_FILES
