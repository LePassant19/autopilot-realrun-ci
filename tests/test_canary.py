"""Preuves exécutables de STORY-009 : CANARY.md porte la date UTC du jour, et
seuls CANARY.md + ce fichier changent par rapport à main."""
import re
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
ALLOWED_CHANGED_FILES = {"CANARY.md", "tests/test_canary.py"}


def _parse_canary_date() -> date:
    match = re.search(r"canary (\S+)", CANARY_PATH.read_text(encoding="utf-8"))
    assert match, "CANARY.md doit contenir une ligne 'canary <date>'"
    return date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_utc_date():
    assert CANARY_PATH.exists(), "CANARY.md doit exister à la racine"
    today_utc = datetime.now(timezone.utc).date()
    assert _parse_canary_date() == today_utc


def test_ac2_canary_line_matches_today_utc():
    today_utc = datetime.now(timezone.utc).date()
    assert _parse_canary_date() == today_utc


def _merge_base_ref() -> str:
    for ref in ("origin/main", "main"):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        if result.returncode == 0:
            return ref
    raise AssertionError("ni origin/main ni main ne sont résolvables")


def test_ac3_only_canary_files_changed_since_merge_base():
    ref = _merge_base_ref()
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", ref],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()
    diff = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    changed_files = {line for line in diff.stdout.splitlines() if line}
    assert changed_files <= ALLOWED_CHANGED_FILES, changed_files
