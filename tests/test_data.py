import pandas as pd
import pytest

from src.data import load_reviews, load_tokenized_reviews, tokenize_reviews


def test_load_reviews_returns_text_column(tmp_path):
    csv = tmp_path / "mini.csv"
    pd.DataFrame(
        {"sentiment": ["Positive", "Negative"], "review": ["Great film", "Bad film"]}
    ).to_csv(csv, index=False)
    assert load_reviews(csv) == ["Great film", "Bad film"]


def test_load_reviews_missing_column_raises(tmp_path):
    csv = tmp_path / "bad.csv"
    pd.DataFrame({"text": ["x"]}).to_csv(csv, index=False)
    with pytest.raises(KeyError):
        load_reviews(csv)


def test_tokenize_reviews():
    result = tokenize_reviews(["The great movie", "A terrible film"])
    assert result == [["great", "movie"], ["terrible", "film"]]


def test_load_tokenized_reviews(tmp_path):
    csv = tmp_path / "mini.csv"
    pd.DataFrame({"review": ["The great movie"]}).to_csv(csv, index=False)
    assert load_tokenized_reviews(csv) == [["great", "movie"]]
