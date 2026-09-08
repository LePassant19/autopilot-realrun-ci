import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"
LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _read_canary_date() -> datetime.date:
    content = CANARY_PATH.read_text()
    match = LINE_RE.search(content)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_has_today_date():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _read_canary_date() == today_utc


def test_ac2_canary_line_is_parseable():
    content = CANARY_PATH.read_text()
    match = LINE_RE.search(content)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    parsed = datetime.date.fromisoformat(match.group(1))
    assert isinstance(parsed, datetime.date)
