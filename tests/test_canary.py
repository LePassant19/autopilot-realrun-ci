import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"
LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def _canary_date() -> datetime.date:
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = LINE_RE.search(content)
    assert match, f"no 'canary <date>' line found in {CANARY_PATH}"
    return datetime.date.fromisoformat(match.group(1))


def test_ac1_canary_file_contains_today_utc_date():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _canary_date() == today_utc


def test_ac2_pytest_proves_canary_date_matches_utc_today():
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert _canary_date() == today_utc
