import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"


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
