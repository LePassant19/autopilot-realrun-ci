"""Preuves exécutables AC1..AC3 de STORY-009 (canari)."""
import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _today_utc() -> datetime.date:
    return datetime.datetime.now(datetime.timezone.utc).date()


def _canary_date() -> datetime.date:
    match = CANARY_LINE_RE.search(CANARY_PATH.read_text(encoding="utf-8"))
    assert match is not None, "aucune ligne `canary <date>` trouvée dans CANARY.md"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_file_exists_with_today_canary_line():
    assert CANARY_PATH.exists()
    assert _canary_date() == _today_utc()


def test_ac2_canary_date_parses_as_today_utc():
    assert _canary_date() == _today_utc()


def _merge_base_ref() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return "origin/main" if result.returncode == 0 else "main"


def test_ac3_only_canary_files_changed():
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", _merge_base_ref()],
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

    allowed = {"CANARY.md", "tests/test_canary.py"}
    assert set(diff) <= allowed, f"fichiers hors périmètre modifiés : {set(diff) - allowed}"
