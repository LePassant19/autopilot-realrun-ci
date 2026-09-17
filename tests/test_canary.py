import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_CHANGED_FILES = {"CANARY.md", "tests/test_canary.py"}


def test_ac2_canary_date_is_today_utc():
    content = (REPO_ROOT / "CANARY.md").read_text()
    match = re.search(r"^canary (\S+)$", content, re.MULTILINE)
    assert match, f"aucune ligne 'canary <date>' trouvée dans CANARY.md : {content!r}"
    canary_date = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc


def _ref_exists(ref):
    result = subprocess.run(
        ["git", "rev-parse", "--verify", ref],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def test_ac3_only_canary_files_changed():
    base_ref = "origin/main" if _ref_exists("origin/main") else "main"
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", base_ref],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    diff_output = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    changed_files = {line for line in diff_output.splitlines() if line}
    assert changed_files <= ALLOWED_CHANGED_FILES, changed_files
