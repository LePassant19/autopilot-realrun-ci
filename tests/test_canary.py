import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"

CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def test_ac2_canary_date_is_today_utc():
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = CANARY_LINE_RE.search(content)
    assert match, f"no 'canary YYYY-MM-DD' line found in {CANARY_PATH}"

    canary_date = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc


def _merge_base_ref() -> str:
    for ref in ("origin/main", "main"):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return ref
    raise AssertionError("neither origin/main nor main is resolvable")


def test_ac3_scope_is_limited_to_canary_files():
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
    assert set(diff) <= allowed
