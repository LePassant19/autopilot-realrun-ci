import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\S+)$", content, re.MULTILINE)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_utc_date():
    assert CANARY_PATH.is_file()
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today_utc


def test_ac2_canary_date_matches_utc_today():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    parsed_date = _read_canary_date()
    assert isinstance(parsed_date, datetime.date)
    assert parsed_date == today_utc


def _merge_base_with_main() -> str:
    for ref in ("main", "origin/main"):
        result = subprocess.run(
            ["git", "merge-base", "HEAD", ref],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    raise RuntimeError("no local or remote 'main' ref found to diff against")


def test_ac3_only_canary_files_changed_since_main():
    base = _merge_base_with_main()
    changed = subprocess.run(
        ["git", "diff", "--name-only", base, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert changed, "expected the canary story to add/modify at least one file"
    assert set(changed) <= {"CANARY.md", "tests/test_canary.py"}
