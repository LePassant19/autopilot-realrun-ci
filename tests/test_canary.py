import datetime
import pathlib
import re
import subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"

CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text()
    match = CANARY_LINE_RE.search(content)
    assert match, f"no 'canary YYYY-MM-DD' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_date():
    assert CANARY_PATH.exists(), f"{CANARY_PATH} does not exist"
    today = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today


def test_ac2_canary_date_parses_and_matches_utc_today():
    canary_date = _read_canary_date()
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

    allowed = {"CANARY.md", "tests/test_canary.py"}
    changed = {path for path in diff if path}
    assert changed <= allowed, f"unexpected files changed: {changed - allowed}"
