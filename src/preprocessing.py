"""Text preprocessing for the movie-review corpus.

A single, importable normalisation pipeline used by training, the notebook, and
the Streamlit app. Keeping this in one place guarantees that a word typed into
the app is normalised exactly the way the training corpus was, so lookups hit
the same vocabulary the model was trained on.
"""

from __future__ import annotations

import re
import unicodedata

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Tokens shorter than this are dropped (removes most punctuation-only and
# low-signal fragments), matching the original project's behaviour.
MIN_TOKEN_LEN = 3

_HTML_BREAK_RE = re.compile(r"<br\s*/?>")
_NON_LETTER_RE = re.compile(r"[^a-z]+")

# Lazily initialised so importing this module never triggers a network call.
_STOPWORDS: set[str] | None = None


def ensure_nltk_data() -> None:
    """Download the NLTK resources this module needs, non-interactively.

    Safe to call repeatedly; ``nltk.download`` is a no-op when data is present.
    ``punkt_tab`` is required by newer NLTK versions for ``word_tokenize``.
    """
    for resource in ("stopwords", "punkt", "punkt_tab"):
        nltk.download(resource, quiet=True)


def _get_stopwords() -> set[str]:
    global _STOPWORDS
    if _STOPWORDS is None:
        ensure_nltk_data()
        _STOPWORDS = set(stopwords.words("english"))
    return _STOPWORDS


def unicode_to_ascii(s: str) -> str:
    """Strip accents by decomposing to NFD and dropping combining marks."""
    return "".join(
        c
        for c in unicodedata.normalize("NFD", str(s))
        if unicodedata.category(c) != "Mn"
    )


def preprocess(text: str) -> list[str]:
    """Normalise a raw review into a list of content tokens.

    Lower-cases, strips accents and HTML line breaks, keeps only alphabetic
    characters, removes English stop words and tokens shorter than
    :data:`MIN_TOKEN_LEN`.
    """
    cleaned = unicode_to_ascii(str(text).lower())
    cleaned = _HTML_BREAK_RE.sub(" ", cleaned)
    cleaned = _NON_LETTER_RE.sub(" ", cleaned)
    stop = _get_stopwords()
    return [
        token
        for token in word_tokenize(cleaned)
        if len(token) >= MIN_TOKEN_LEN and token not in stop
    ]


def normalize_word(word: str) -> str | None:
    """Normalise a single user-supplied word the same way training does.

    Returns the normalised token, or ``None`` if the input reduces to nothing
    (e.g. a stop word or punctuation). Used by the app to look up user input.
    """
    tokens = preprocess(word)
    return tokens[0] if tokens else None
