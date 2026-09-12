import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = CANARY_LINE_RE.search(content)
    assert match, f"no 'canary YYYY-MM-DD' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_file_exists_with_today_line():
    assert CANARY_PATH.is_file()
    _read_canary_date()


def test_ac2_date_matches_utc_today():
    canary_date = _read_canary_date()
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc
