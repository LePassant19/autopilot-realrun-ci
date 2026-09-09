import datetime
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
SMOKE_PATH = REPO_ROOT / "tests" / "test_smoke.py"
CANARY_LINE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
STORY_FILES = {"CANARY.md", "tests/test_canary.py"}


def _canary_line_match() -> re.Match | None:
    return CANARY_LINE.search(CANARY_PATH.read_text(encoding="utf-8"))


def test_ac1_canary_md_exists_at_root_with_a_canary_date_line():
    assert CANARY_PATH.is_file(), f"{CANARY_PATH} absent de la racine du dépôt"
    assert _canary_line_match(), "CANARY.md ne contient pas de ligne 'canary YYYY-MM-DD'"


def test_ac2_canary_date_parses_to_today_utc():
    match = _canary_line_match()
    assert match, "CANARY.md ne contient pas de ligne 'canary YYYY-MM-DD'"
    parsed = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert parsed == today_utc, f"CANARY.md date du {parsed}, attendu {today_utc} (UTC)"


def _base_commit() -> str | None:
    for ref in ("main", "origin/main"):
        result = subprocess.run(
            ["git", "merge-base", "HEAD", ref],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    return None


# Un checkout CI superficiel (`actions/checkout@v4`, fetch-depth 1) n'a ni `main` ni `origin/main` :
# la portée du diff y est invérifiable, alors que la gate locale a l'historique complet.
BASE_COMMIT = _base_commit()


@pytest.mark.skipif(BASE_COMMIT is None, reason="aucune base 'main' dans ce checkout")
def test_ac3_smoke_suite_intact_and_no_other_file_touched():
    assert SMOKE_PATH.is_file(), "la suite existante tests/test_smoke.py a disparu"

    # `git diff <base>` (sans `HEAD`) compare la base au working tree : la preuve vaut aussi bien
    # avant qu'après le commit du runner, et ignore les fichiers non suivis.
    changed = subprocess.run(
        ["git", "diff", "--name-only", BASE_COMMIT],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    hors_perimetre = set(filter(None, changed)) - STORY_FILES
    assert not hors_perimetre, f"fichiers hors périmètre de la story : {sorted(hors_perimetre)}"
