import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
SMOKE_PATH = REPO_ROOT / "tests" / "test_smoke.py"
STORY_FILES = {"CANARY.md", "tests/test_canary.py"}


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\d{4}-\d{2}-\d{2})$", content, re.MULTILINE)
    assert match, f"no 'canary YYYY-MM-DD' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_dated_line():
    assert CANARY_PATH.exists(), f"{CANARY_PATH} is missing"
    _read_canary_date()


def test_ac2_canary_date_matches_utc_today():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today_utc


def test_ac3_only_story_files_changed_since_main():
    assert SMOKE_PATH.is_file(), "tests/test_smoke.py existante a disparu"

    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", "main"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert merge_base.returncode == 0, (
        f"impossible de trouver la base 'main' (historique complet requis, "
        f"fetch-depth: 0): {merge_base.stderr}"
    )
    base_commit = merge_base.stdout.strip()

    changed = subprocess.run(
        ["git", "diff", "--name-only", base_commit],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    out_of_scope = set(filter(None, changed)) - STORY_FILES
    assert not out_of_scope, f"fichiers hors périmètre de la story : {sorted(out_of_scope)}"
