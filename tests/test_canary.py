import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _canary_date():
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = CANARY_LINE_RE.search(content)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_date():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _canary_date() == today_utc


def test_ac2_canary_test_is_never_skipped():
    lines = Path(__file__).read_text(encoding="utf-8").splitlines()
    decorator_lines = [line for line in lines if line.strip().startswith("@")]
    forbidden_names = ("skip", "skipif", "xfail")
    for line in decorator_lines:
        assert not any(name in line for name in forbidden_names), line


def _merge_base_ref():
    check = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "origin/main"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return "origin/main" if check.returncode == 0 else "main"


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

    changed = {line.strip() for line in diff if line.strip()}
    allowed = {"CANARY.md", "tests/test_canary.py"}
    assert changed <= allowed, f"unexpected files changed: {changed - allowed}"
