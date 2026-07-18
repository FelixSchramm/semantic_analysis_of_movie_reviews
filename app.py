"""Streamlit demo for the movie-review Word2Vec model.

Explore the learned embeddings interactively:

* **Find similar words** — the 10 nearest neighbours of a word by cosine
  similarity.
* **Word analogies** — vector arithmetic such as ``king - man + woman``.

Run from the repo root with the model artifact present::

    python -m src.train           # produces word2vec.wv (see README / issue #2)
    streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from gensim.models import KeyedVectors

from src.preprocessing import normalize_word

WV_PATH = "word2vec.wv"

st.set_page_config(page_title="Movie-Review Word2Vec", layout="wide")


@st.cache_resource
def load_vectors(path: str = WV_PATH) -> KeyedVectors:
    """Load the trained KeyedVectors (cached for the session)."""
    return KeyedVectors.load(path)


def _lookup(word: str, wv: KeyedVectors) -> tuple[str | None, str | None]:
    """Normalise a user word and check it is in the vocabulary.

    Returns ``(token, error)`` where exactly one element is not ``None``.
    """
    token = normalize_word(word)
    if token is None:
        return None, f"'{word}' reduces to nothing after preprocessing (stop word or punctuation)."
    if token not in wv:
        return None, f"'{token}' is not in the model vocabulary."
    return token, None


st.title("Word2Vec — Semantic Analysis of Movie Reviews")
st.caption(
    "Word embeddings trained with gensim on 25,000 movie reviews. "
    "Words are normalised with the same preprocessing used at training time."
)

if not Path(WV_PATH).exists():
    st.error(
        f"Model artifact '{WV_PATH}' not found. Train it first with "
        "`python -m src.train` (see the README) or download it from the release."
    )
    st.stop()

wv = load_vectors()

# --- Similarity -----------------------------------------------------------
st.header("Find similar words")
sim_word = st.text_input("Enter a word:", "movie")
if st.button("Find similar"):
    token, error = _lookup(sim_word, wv)
    if error:
        st.warning(error)
    else:
        results = wv.most_similar(token, topn=10)
        st.subheader(f"Words most similar to '{token}'")
        st.table(
            {
                "word": [w for w, _ in results],
                "cosine similarity": [round(float(s), 3) for _, s in results],
            }
        )

# --- Analogies ------------------------------------------------------------
st.header("Word analogies")
st.write("Solve *word1 − word2 + word3*, e.g. `king − man + woman`.")
col1, col2, col3 = st.columns(3)
w1 = col1.text_input("word1 (add)", "king")
w2 = col2.text_input("word2 (subtract)", "man")
w3 = col3.text_input("word3 (add)", "woman")
if st.button("Solve analogy"):
    t1, e1 = _lookup(w1, wv)
    t2, e2 = _lookup(w2, wv)
    t3, e3 = _lookup(w3, wv)
    errors = [e for e in (e1, e2, e3) if e]
    if errors:
        for e in errors:
            st.warning(e)
    else:
        results = wv.most_similar(positive=[t1, t3], negative=[t2], topn=5)
        st.subheader(f"{t1} − {t2} + {t3} ≈")
        st.table(
            {
                "word": [w for w, _ in results],
                "cosine similarity": [round(float(s), 3) for _, s in results],
            }
        )
