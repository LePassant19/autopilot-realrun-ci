import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"


def test_ac2_readme_documents_python_versions():
    text = README.read_text(encoding="utf-8")
    match = re.search(r"^## CI\n(.*?)(?=\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, "README.md doit contenir une section '## CI'"
    section = match.group(1)
    assert "3.11" in section
    assert "3.12" in section
