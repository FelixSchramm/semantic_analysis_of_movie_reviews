"""Train a Word2Vec model on the movie-review corpus and save the vectors.

Run as a script from the repo root::

    python -m src.train --data MovieReview.csv --out .

This produces two artifacts:

* ``word2vec.model`` — the full gensim model (can be loaded to resume training).
* ``word2vec.wv``    — the ``KeyedVectors`` used by the app for similarity and
  analogy queries (smaller; all the app needs).

Because gensim stores the vocabulary inside the model, there is no separate
tokenizer to persist and keep in sync — the word→vector mapping travels with the
vectors, which removes the train/serve skew the previous Keras setup suffered.
"""

from __future__ import annotations

import argparse
import logging
import random
from pathlib import Path

import numpy as np
from gensim.models import Word2Vec

from .data import load_tokenized_reviews
from .preprocessing import ensure_nltk_data

# Fixed hyper-parameters (defined once, so "the model" is a reproducible object).
VECTOR_SIZE = 100
WINDOW = 5
MIN_COUNT = 5
EPOCHS = 10
SG = 0  # 0 = CBOW (matches the project's original Continuous-Bag-of-Words aim)
SEED = 42

logger = logging.getLogger(__name__)


def train_word2vec(csv_path: str | Path, workers: int = 1) -> Word2Vec:
    """Train and return a Word2Vec model on the reviews in ``csv_path``.

    ``workers`` defaults to 1 for deterministic, reproducible training (with the
    fixed :data:`SEED`). Increase it to speed training up at the cost of exact
    reproducibility (gensim's OS-thread scheduling makes multi-worker runs
    non-deterministic even with a fixed seed).
    """
    random.seed(SEED)
    np.random.seed(SEED)
    ensure_nltk_data()

    logger.info("Loading and tokenising %s ...", csv_path)
    sentences = load_tokenized_reviews(csv_path)
    logger.info("Training Word2Vec on %d reviews ...", len(sentences))

    model = Word2Vec(
        sentences=sentences,
        vector_size=VECTOR_SIZE,
        window=WINDOW,
        min_count=MIN_COUNT,
        sg=SG,
        epochs=EPOCHS,
        seed=SEED,
        workers=workers,
    )
    logger.info("Done. Vocabulary size: %d", len(model.wv))
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the movie-review Word2Vec model.")
    parser.add_argument("--data", default="MovieReview.csv", help="Path to the reviews CSV.")
    parser.add_argument("--out", default=".", help="Directory to write the artifacts to.")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Training threads (1 = reproducible; higher = faster, non-deterministic).",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    model = train_word2vec(args.data, workers=args.workers)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    model.save(str(out / "word2vec.model"))
    model.wv.save(str(out / "word2vec.wv"))
    logger.info("Saved word2vec.model and word2vec.wv to %s", out.resolve())


if __name__ == "__main__":
    main()
