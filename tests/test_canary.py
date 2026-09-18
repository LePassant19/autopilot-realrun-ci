import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _canary_date_str() -> str:
    match = CANARY_LINE_RE.search(CANARY_PATH.read_text(encoding="utf-8"))
    assert match, "CANARY.md doit contenir une ligne 'canary YYYY-MM-DD'"
    return match.group(1)


def test_ac1_canary_file_has_today_line():
    assert CANARY_PATH.exists()
    assert _canary_date_str()


def test_ac2_canary_date_matches_utc_today():
    canary_date = datetime.date.fromisoformat(_canary_date_str())
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc


def _merge_base_ref() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return "origin/main" if result.returncode == 0 else "main"


def test_ac3_diff_limited_to_canary_files():
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
    allowed = {"CANARY.md", "tests/test_canary.py"}
    assert changed <= allowed, f"fichiers hors périmètre modifiés : {changed - allowed}"
