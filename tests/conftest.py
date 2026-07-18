import pytest

from src.preprocessing import ensure_nltk_data


@pytest.fixture(scope="session", autouse=True)
def _nltk_data() -> None:
    """Download the NLTK resources the preprocessing tests need, once per session."""
    ensure_nltk_data()
