"""Canari STORY-009 : preuve exécutable d'AC1, AC2 et AC3."""
import datetime
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
ALLOWED_CHANGED_FILES = {"CANARY.md", "tests/test_canary.py"}


def _canary_date() -> datetime.date:
    text = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\S+)$", text, re.MULTILINE)
    assert match is not None, f"ligne 'canary <date>' introuvable dans {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def _utc_today() -> datetime.date:
    return datetime.datetime.now(datetime.timezone.utc).date()


def _merge_base_ref() -> str:
    for ref in ("origin/main", "main"):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", ref],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return ref
    raise AssertionError("ni origin/main ni main ne sont résolvables")


def test_ac1_file_contains_canary_line_for_today():
    assert CANARY_PATH.is_file(), "CANARY.md doit exister à la racine"
    assert _canary_date() == _utc_today()


def test_ac2_date_matches_utc_today():
    assert _canary_date() == datetime.datetime.now(datetime.timezone.utc).date()


def test_ac3_only_canary_files_changed():
    base_ref = _merge_base_ref()
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", base_ref],
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
    assert changed <= ALLOWED_CHANGED_FILES, (
        f"fichiers modifiés hors périmètre du canari : {changed - ALLOWED_CHANGED_FILES}"
    )
