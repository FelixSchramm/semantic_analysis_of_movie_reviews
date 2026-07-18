"""Reusable building blocks for the movie-review Word2Vec project.

The functions here are the single source of truth for text preprocessing and
corpus loading. They are imported by the training entry point, the notebook, and
the Streamlit app so that text is normalised identically everywhere (avoiding
train/serve skew).
"""

from .preprocessing import (
    ensure_nltk_data,
    normalize_word,
    preprocess,
    unicode_to_ascii,
)
from .data import load_reviews, load_tokenized_reviews, tokenize_reviews

__all__ = [
    "ensure_nltk_data",
    "normalize_word",
    "preprocess",
    "unicode_to_ascii",
    "load_reviews",
    "tokenize_reviews",
    "load_tokenized_reviews",
]
