import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"

CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _canary_date() -> datetime.date:
    text = CANARY_PATH.read_text(encoding="utf-8")
    match = CANARY_LINE_RE.search(text)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def _today_utc() -> datetime.date:
    return datetime.datetime.now(datetime.timezone.utc).date()


def test_ac1_canary_file_has_today_utc_date():
    assert CANARY_PATH.is_file()
    assert _canary_date() == _today_utc()


def test_ac2_canary_date_matches_utc_today():
    assert _canary_date() == _today_utc()


def _merge_base_ref() -> str:
    for ref in ("origin/main", "main"):
        result = subprocess.run(
            ["git", "merge-base", "HEAD", ref],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    raise AssertionError("neither origin/main nor main is available for merge-base")


def test_ac3_only_canary_files_changed():
    merge_base = _merge_base_ref()
    result = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    changed = {line for line in result.stdout.splitlines() if line}
    allowed = {"CANARY.md", "tests/test_canary.py"}
    assert changed <= allowed, f"unexpected files changed: {changed - allowed}"
