import datetime
import re
from pathlib import Path

CANARY_PATH = Path(__file__).resolve().parent.parent / "CANARY.md"


def test_ac2_canary_date_matches_today_utc():
    content = CANARY_PATH.read_text(encoding="utf-8")
    match = re.search(r"^canary (\d{4}-\d{2}-\d{2})$", content, re.MULTILINE)
    assert match is not None, f"no 'canary <date>' line found in {CANARY_PATH}"

    canary_date = datetime.date.fromisoformat(match.group(1))
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    assert canary_date == today_utc
