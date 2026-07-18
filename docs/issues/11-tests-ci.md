# Issue 11: Add tests and CI (ruff + pytest on synthetic data)

**Priority:** P1 — There are no tests and no CI, so nothing guards the
preprocessing/CBOW logic or lints the code. A green CI badge and a small test
suite are strong, cheap professionalism signals for a portfolio repo.
**Affects:** new `tests/`, new `.github/workflows/ci.yml`, `requirements.txt`

## Context

`git ls-files` shows no `tests/` and no `.github/workflows/`. The logic most
worth testing (preprocessing normalisation, CBOW context/target pairing) is
deterministic and can be checked on **tiny synthetic inputs**, so CI does not
need the 32 MB dataset or a trained model.

## Goal

A minimal but real test suite covers the core functions on small synthetic data,
and a CI workflow runs linting and tests on every push/PR without requiring the
full dataset or GPU training.

## Implementation steps

1. Depends on Issue 10 (#TBD): tests import from `src/`.
2. Add `tests/` with `pytest` cases on synthetic inputs, e.g.:
   - `preprocess_sentence("The CATS!! running 12 times.")` lowercases, strips
     punctuation/short tokens, and removes stopwords as specified.
   - `create_cbow_data(["a b c d e"], window_size=1, ...)` returns context/target
     pairs of the expected shapes and values on a hand-checkable corpus.
   - Use `pandas.testing.assert_frame_equal` where a DataFrame is compared.
3. Add `ruff` as the single lint/format tool; add a `ruff.toml` or `[tool.ruff]`
   config and fix or explicitly ignore findings.
4. Add `.github/workflows/ci.yml` that, on push and PR:
   - sets up the pinned Python version (Issue 09 (#TBD)),
   - installs dependencies,
   - runs `ruff check .` and `pytest -q`.
   Keep it CPU-only and dataset-free (tests use synthetic data).
5. Add `pytest` and `ruff` to a dev-requirements list (or `requirements.txt`).

## Affected files

- `tests/test_preprocessing.py`, `tests/test_data.py` (new)
- `.github/workflows/ci.yml` (new)
- `ruff.toml` or `pyproject.toml` (new/updated)
- `requirements.txt` (dev deps)

## Acceptance criteria

- [ ] `pytest -q` passes locally using only synthetic data (no `MovieReview.csv`,
      no trained model required).
- [ ] `ruff check .` passes (or has an explicit, documented ignore set).
- [ ] A CI workflow runs ruff + pytest on push and PR and is green.
- [ ] Tests import the shared functions from `src/`.

## Dependencies

- **Requires Issue 10 (#TBD)** (importable `src/` package) and the pinned Python
  version from Issue 09 (#TBD).
