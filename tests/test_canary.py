import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _parsed_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = CANARY_LINE_RE.search(content)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_utc_date():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _parsed_canary_date() == today_utc


def test_ac2_canary_line_matches_utc_today():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    parsed_date = _parsed_canary_date()
    assert parsed_date == today_utc, (
        f"CANARY.md date {parsed_date.isoformat()} does not match "
        f"UTC today {today_utc.isoformat()}"
    )
