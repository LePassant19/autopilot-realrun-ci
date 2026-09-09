import datetime
import pathlib
import re

CANARY_PATH = pathlib.Path(__file__).resolve().parent.parent / "CANARY.md"


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text()
    match = re.search(r"^canary (\S+)$", content, flags=re.MULTILINE)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_utc_date():
    assert CANARY_PATH.is_file()
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today_utc


def test_ac2_canary_date_matches_today_utc():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today_utc
