import datetime
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANARY = ROOT / "CANARY.md"
ALLOWED_CHANGES = {"CANARY.md", "tests/test_canary.py"}
CANARY_LINE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _canary_date_text() -> str:
    match = CANARY_LINE.search(CANARY.read_text(encoding="utf-8"))
    assert match, "CANARY.md ne contient aucune ligne `canary YYYY-MM-DD`"
    return match.group(1)


def test_ac1_canary_md_has_a_canary_line():
    assert CANARY.is_file(), "CANARY.md doit exister à la racine du dépôt"
    assert CANARY_LINE.search(CANARY.read_text(encoding="utf-8"))


def test_ac2_canary_date_is_today_utc():
    recorded = datetime.date.fromisoformat(_canary_date_text())
    today = datetime.datetime.now(datetime.timezone.utc).date()
    assert recorded == today


def test_ac3_only_canary_files_changed():
    has_origin_main = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "origin/main"],
        cwd=ROOT,
        capture_output=True,
    ).returncode == 0
    base = _git("merge-base", "HEAD", "origin/main" if has_origin_main else "main")
    changed = set(_git("diff", "--name-only", base).splitlines())
    assert changed <= ALLOWED_CHANGES, f"fichiers hors périmètre : {sorted(changed - ALLOWED_CHANGES)}"
