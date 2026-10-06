"""Preuves exécutables d'AC1/AC2/AC3 de STORY-009 (canari)."""
import datetime
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANARY = ROOT / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _canary_date() -> datetime.date:
    match = CANARY_LINE_RE.search(CANARY.read_text(encoding="utf-8"))
    assert match, f"no 'canary YYYY-MM-DD' line found in {CANARY}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_declares_a_date():
    assert CANARY.exists()
    assert isinstance(_canary_date(), datetime.date)


def test_ac2_canary_date_is_todays_utc_date():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    assert _canary_date() == today


def test_ac3_only_canary_files_are_touched():
    target = "origin/main"
    if subprocess.run(
        ["git", "rev-parse", "--verify", target],
        cwd=ROOT, capture_output=True, text=True,
    ).returncode != 0:
        target = "main"

    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", target],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()

    changed = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.splitlines()

    allowed = {"CANARY.md", "tests/test_canary.py"}
    assert set(changed) <= allowed, f"fichiers hors périmètre : {set(changed) - allowed}"
