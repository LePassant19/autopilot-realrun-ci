import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"
CANARY_LINE_RE = re.compile(r"^canary (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def test_ac1_canary_file_has_today_date():
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = CANARY_LINE_RE.search(content)
    assert match is not None, "no 'canary YYYY-MM-DD' line found in CANARY.md"

    canary_date = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc
