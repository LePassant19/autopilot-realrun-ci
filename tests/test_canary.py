from datetime import date
from pathlib import Path


def test_ac2_canary_md_contains_valid_iso_date():
    content = Path("CANARY.md").read_text(encoding="utf-8")
    line = next(
        (l for l in content.splitlines() if l.startswith("canary ")), None
    )
    assert line is not None, "CANARY.md doit contenir une ligne 'canary <date>'"
    raw_date = line[len("canary "):].strip()
    date.fromisoformat(raw_date)
