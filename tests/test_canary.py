from datetime import date, datetime, timezone
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"


def _canary_date():
    content = CANARY_PATH.read_text(encoding="utf-8")
    line = next(
        (l for l in content.splitlines() if l.startswith("canary ")), None
    )
    assert line is not None, "CANARY.md doit contenir une ligne 'canary <date>'"
    raw_date = line[len("canary "):].strip()
    return date.fromisoformat(raw_date)


def test_ac2_canary_md_contains_valid_iso_date():
    _canary_date()


def test_ac1_canary_date_is_today_utc():
    assert _canary_date() == datetime.now(timezone.utc).date()
