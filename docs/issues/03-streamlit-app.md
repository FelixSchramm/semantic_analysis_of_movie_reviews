# Issue 03: Ship the real Streamlit app as `app.py` and fix its runtime bugs

**Priority:** P0 — The README advertises an interactive Streamlit demo, but the
checked-in `app.py` is a course training script, not that app. If deployed as-is
the demo is broken. This directly contradicts the repo's headline feature.
**Affects:** `app.py`

## Context

There are two different, conflicting `app.py` definitions:

- The **checked-in `app.py`** imports `streamlit as st` but never calls it. It is
  the DataScientest training exercise: it contains checklist comments `# (a)`
  through `# (j)`, an interactive `nltk.download()` (`app.py:29`), a trailing
  `df.head()` (`app.py:53`), and it ends by training and saving a model. It is
  not a web app.
- The **real Streamlit app** exists only inside `code.ipynb` cell 12 as a
  `%%writefile app.py` block. It was never written out to the tracked `app.py`.
  That app also has two defects:
  1. It calls `pd.read_csv(...)` but **never imports pandas** → `NameError` at
     runtime.
  2. It re-creates a tokenizer by fitting on the **raw** `df.review`
     (un-preprocessed), whereas the model was trained on **preprocessed** text.
     The word→index mapping therefore does not match the embedding matrix, so
     "similar words" and analogies are computed against mismatched indices
     (train/serve skew).

## Goal

The tracked `app.py` is the working Streamlit application: it loads the persisted
model and tokenizer from Issue 02 (#TBD), applies the **same** preprocessing used
in training, and correctly returns nearest neighbours and analogies. Deploying
`app.py` yields the demo the README describes.

## Implementation steps

1. Replace the entire contents of the tracked `app.py` with the Streamlit app
   (base it on notebook cell 12), deleting the course training script.
2. Add the missing `import pandas as pd` (and remove any unused imports).
3. Do **not** re-fit a tokenizer at serve time. Load the persisted artifact from
   Issue 02 (#TBD):
   ```python
   import pickle
   with open("tokenizer.pkl", "rb") as f:
       tokenizer = pickle.load(f)
   word2idx = tokenizer.word_index
   idx2word = tokenizer.index_word
   ```
4. Reuse the **single** shared preprocessing function (see Issue 10 (#TBD)) for
   any user-entered word before looking it up, so serve-time and train-time text
   are normalised identically.
5. Guard against out-of-vocabulary input and indices `>= num_words` gracefully
   (the app already has some guards; keep them and cover the analogy path too).
6. Keep the model source of truth as `word2vec.h5`/`.keras` produced by
   Issue 02 (#TBD); do not train inside the app.
7. Smoke-test locally: `streamlit run app.py`, confirm both "Find Similar" and
   "Calculate Analogy" return results without a traceback.

## Affected files

- `app.py`

## Acceptance criteria

- [ ] `app.py` contains a Streamlit app (uses `st.` widgets) and no training
      code, no `# (a)`–`# (j)` comments, and no `nltk.download()`.
- [ ] `app.py` imports every module it uses (including pandas, if still needed).
- [ ] The app loads `tokenizer.pkl` rather than re-fitting a tokenizer, so its
      indices match the trained embedding matrix.
- [ ] User input is passed through the same preprocessing function as training.
- [ ] `streamlit run app.py` starts and both features return results without an
      exception.

## Dependencies

- **Requires Issue 02 (#TBD)** (persisted `word2vec` model + `tokenizer.pkl`).
- Uses the shared preprocessing function from Issue 10 (#TBD) if that is done
  first; otherwise inline the identical preprocessing and refactor later.
