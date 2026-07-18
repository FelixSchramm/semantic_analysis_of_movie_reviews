# Issue 02: Make the trained model and tokenizer reproducible and available

**Priority:** P0 — The app the README advertises cannot run without a trained
model, and the repo neither ships one nor provides a deterministic way to
regenerate it together with the tokenizer it depends on.
**Affects:** `code.ipynb`, new `src/train.py` (see Issue 10 (#TBD)), `word2vec.h5`,
new `tokenizer.pkl`, new `.gitattributes`

## Context

- `git ls-files` shows no `word2vec.h5`. The notebook's `app.py` (cell 12) and
  the deployment notes both call `load_model('word2vec.h5')`, which fails with no
  artifact present.
- The model and the tokenizer are coupled: the embedding matrix row *i* only
  means something together with the tokenizer that assigned index *i*. Today the
  tokenizer is re-created ad hoc at serve time (see Issue 03 (#TBD)), which breaks
  that coupling. The tokenizer (and the exact preprocessing) must be persisted
  **alongside** the model.
- Epoch counts are inconsistent across the history (notebook cell 10 uses 5;
  earlier course material implied 50), so "the model" is not a fixed object.

## Goal

A single, deterministic training entry point produces **both** `word2vec.h5` and
a persisted `tokenizer.pkl` from `MovieReview.csv`, with a fixed random seed and
a fixed epoch count. The artifacts are made available to the app either via Git
LFS or a GitHub Release, and are excluded from normal git tracking otherwise.

## Implementation steps

1. In the training code (notebook cell that trains, and/or `src/train.py` from
   Issue 10 (#TBD)), set seeds once at the top:
   `import numpy as np, tensorflow as tf; np.random.seed(42); tf.random.set_seed(42)`.
2. After `tokenizer.fit_on_texts(...)`, persist the tokenizer so serving reuses
   the exact same vocabulary:
   ```python
   import pickle
   with open("tokenizer.pkl", "wb") as f:
       pickle.dump(tokenizer, f)
   ```
   Save the model with `model.save("word2vec.h5")` (or the native
   `model.save("word2vec.keras")` format, which is preferred on modern Keras).
3. Fix the epoch count to a single documented value (e.g. `EPOCHS = 20`) defined
   once; do not have different numbers in different files.
4. Choose an artifact distribution strategy and document it in the README
   (coordinate with Issue 04 (#TBD) and Issue 08 (#TBD)):
   - **Preferred:** attach `word2vec.h5`/`word2vec.keras` + `tokenizer.pkl` to a
     GitHub Release and download them in the app / a `make` target; **or**
   - track them with Git LFS:
     ```bash
     git lfs install
     git lfs track "*.h5" "*.keras" "*.pkl"
     git add .gitattributes
     ```
5. Ensure the model artifacts are git-ignored when not tracked via LFS (see
   Issue 06 (#TBD)).

## Affected files

- `code.ipynb` (seed, epoch constant, tokenizer persistence)
- `src/train.py` (if Issue 10 (#TBD) is done first)
- `word2vec.h5` / `word2vec.keras`, `tokenizer.pkl` (produced artifacts)
- `.gitattributes` (only if using Git LFS)

## Acceptance criteria

- [ ] Running the training entry point from a clean checkout produces both
      `word2vec.h5` (or `.keras`) and `tokenizer.pkl`.
- [ ] A random seed is set so repeated runs are reproducible.
- [ ] The epoch count is defined exactly once and is consistent across notebook,
      script, and README.
- [ ] The README documents where to obtain or how to regenerate the model, and
      the app can locate it without manual edits.

## Dependencies

- Coordinates with Issue 03 (#TBD) (app must load the persisted tokenizer),
  Issue 06 (#TBD) (gitignore), Issue 08 (#TBD) (large-file handling), and
  Issue 10 (#TBD) (if training is moved into `src/`).
