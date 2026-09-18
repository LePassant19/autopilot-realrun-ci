"""Vérifie que le README documente les versions de Python couvertes par la CI (STORY-010 AC2)."""
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"


def test_ac2_readme_documents_ci_python_versions():
    text = README.read_text(encoding="utf-8")
    assert "## CI" in text
    section = text.split("## CI", 1)[1]
    assert "3.11" in section
    assert "3.12" in section
