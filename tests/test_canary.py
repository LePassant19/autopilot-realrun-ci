"""Preuve exécutable d'AC1 (contenu de CANARY.md) et d'AC3 (périmètre du diff)."""
import datetime
import re
import subprocess
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"
ALLOWED_FILES = {"CANARY.md", "tests/test_canary.py"}


def _merge_base_ref() -> str:
    for ref in ("origin/main", "main"):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return ref
    raise RuntimeError("ni origin/main ni main n'existent")


def test_ac2_canary_date_is_today_utc():
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\S+)$", content, re.MULTILINE)
    assert match is not None, "aucune ligne `canary <date>` trouvée dans CANARY.md"

    canary_date = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc


def test_ac3_diff_scope_is_limited_to_canary_files():
    ref = _merge_base_ref()
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", ref],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    diff = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    changed_files = {line.strip() for line in diff if line.strip()}
    assert changed_files <= ALLOWED_FILES
