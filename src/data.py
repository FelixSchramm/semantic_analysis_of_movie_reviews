"""Loading and tokenising the movie-review corpus."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .preprocessing import preprocess

DEFAULT_TEXT_COLUMN = "review"


def load_reviews(csv_path: str | Path, text_column: str = DEFAULT_TEXT_COLUMN) -> list[str]:
    """Read the raw review texts from ``csv_path``.

    Only the text column is returned; the ``sentiment`` column (if present) is
    unused because Word2Vec training is unsupervised.
    """
    df = pd.read_csv(csv_path)
    if text_column not in df.columns:
        raise KeyError(
            f"Column {text_column!r} not found in {csv_path}; "
            f"available columns: {list(df.columns)}"
        )
    return df[text_column].astype(str).tolist()


def tokenize_reviews(reviews: list[str]) -> list[list[str]]:
    """Apply :func:`~src.preprocessing.preprocess` to each review."""
    return [preprocess(review) for review in reviews]


def load_tokenized_reviews(
    csv_path: str | Path, text_column: str = DEFAULT_TEXT_COLUMN
) -> list[list[str]]:
    """Convenience wrapper: load and tokenise in one call.

    The result is exactly the ``sentences`` argument ``gensim.models.Word2Vec``
    expects.
    """
    return tokenize_reviews(load_reviews(csv_path, text_column))
