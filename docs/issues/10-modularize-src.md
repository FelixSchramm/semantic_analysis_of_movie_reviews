# Issue 10: Extract an importable `src/` package

**Priority:** P1 — Core logic (preprocessing, CBOW data creation, training)
currently lives only inside notebook cells and a monolithic script, so nothing
can be imported, reused by the app, or unit-tested. Modularisation is what lets
Issue 03 (#TBD) and Issue 11 (#TBD) share one source of truth.
**Affects:** new `src/` package, `code.ipynb`, `app.py`

## Context

- Preprocessing (`preprocess_sentence`), CBOW pair generation
  (`create_cbow_data`, cell 07), and model construction/training exist only as
  notebook cells and inside the root `app.py`.
- The Streamlit app re-implements preprocessing/tokenisation instead of reusing
  the training code, which is exactly what causes the train/serve skew in
  Issue 03 (#TBD).
- Note: a Python package directory **cannot start with a digit**. If any folder
  is named like `03_src/`, it must be `src/` (or another identifier-safe name)
  to be importable.

## Goal

Reusable logic lives in an importable `src/` package with small, testable
functions. The notebook and `app.py` import from `src/` instead of duplicating
code, so preprocessing is defined exactly once.

## Implementation steps

1. Create a package, e.g.:
   ```
   src/
     __init__.py
     preprocessing.py   # unicode_to_ascii, preprocess_sentence
     data.py            # create_cbow_data(corpus, window_size, ...)
     train.py           # build_model, train, save model + tokenizer (Issue 02)
   ```
   Use an identifier-safe name (no leading digit).
2. Move `preprocess_sentence` and `create_cbow_data` into `src/`, keeping
   signatures stable and adding short docstrings.
3. Refactor `code.ipynb` to `from src.preprocessing import preprocess_sentence`
   etc., rather than defining them inline.
4. Refactor `app.py` (Issue 03 (#TBD)) to import the same `preprocess_sentence`,
   guaranteeing train/serve consistency.
5. Ensure `src/` is importable from the repo root (run from root, or add a
   minimal `pyproject.toml`/`setup.cfg` if you want `pip install -e .`).

## Affected files

- `src/__init__.py`, `src/preprocessing.py`, `src/data.py`, `src/train.py` (new)
- `code.ipynb`
- `app.py`

## Acceptance criteria

- [ ] Preprocessing and CBOW logic live in importable modules under `src/`.
- [ ] The package/directory name is identifier-safe (does not start with a
      digit).
- [ ] `code.ipynb` and `app.py` import these functions instead of redefining
      them.
- [ ] `python -c "from src.preprocessing import preprocess_sentence"` succeeds
      from the repo root.

## Dependencies

- Enables Issue 03 (#TBD) (shared preprocessing) and Issue 11 (#TBD) (unit
  tests); coordinates with Issue 02 (#TBD) (training entry point).
