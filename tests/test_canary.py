import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANARY_PATH = REPO_ROOT / "CANARY.md"
STORY_FILES = {"CANARY.md", "tests/test_canary.py"}


def _canary_date():
    line = next(
        (
            raw
            for raw in CANARY_PATH.read_text(encoding="utf-8").splitlines()
            if raw.startswith("canary ")
        ),
        None,
    )
    assert line is not None, "CANARY.md doit contenir une ligne 'canary <date>'"
    return date.fromisoformat(line[len("canary ") :].strip())


def _git(*args):
    return subprocess.run(
        ("git", *args), cwd=REPO_ROOT, capture_output=True, text=True
    )


def _tracked_files():
    result = _git("ls-files")
    assert result.returncode == 0, result.stderr
    return {name for name in result.stdout.splitlines() if name}


def _story_base():
    for ref in ("origin/main", "main"):
        result = _git("merge-base", "HEAD", ref)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return None


def test_ac1_canary_date_is_today_utc():
    assert _canary_date() == datetime.now(timezone.utc).date()


def test_ac2_canary_md_contains_valid_iso_date():
    _canary_date()


def test_ac3_smoke_stays_green_and_no_other_file_touched():
    import test_smoke

    test_smoke.test_smoke()

    tracked = _tracked_files()
    assert STORY_FILES <= tracked
    assert "uv.lock" not in tracked
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for section in ("[dependency-groups]", "[project.optional-dependencies]"):
        assert section not in pyproject, f"{section} ajoute a pyproject.toml"

    # Le diff complet exige la base de la story dans l'historique : disponible pour le gate
    # local, absente d'un checkout superficiel de CI, ou les invariants ci-dessus tiennent seuls.
    base = _story_base()
    if base is not None:
        diff = _git("diff", "--name-only", base, "--")
        assert diff.returncode == 0, diff.stderr
        touched = {name for name in diff.stdout.splitlines() if name}
        assert touched <= STORY_FILES, f"hors perimetre : {sorted(touched - STORY_FILES)}"
