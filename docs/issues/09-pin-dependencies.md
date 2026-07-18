# Issue 09: Pin dependencies and align the Python version

**Priority:** P1 — Unpinned dependencies make the project non-reproducible: a
future `pip install` can pull incompatible TensorFlow/Keras versions and break
the notebook and app. Reviewers read `requirements.txt` as a reproducibility
signal.
**Affects:** `requirements.txt`, `.python-version`, `README.md`

## Context

- `requirements.txt` lists bare package names with no version constraints, and
  the first line is `tensorflow ` with a trailing space.
- The stated Python version is inconsistent: `README.md:20` says "Python 3.8+",
  `.python-version` is `3.11.9`, and the notebook kernel metadata is `3.9.6`.
- TensorFlow/Keras APIs used here (e.g. `tf.keras.preprocessing.text.Tokenizer`,
  `.h5` saving) are version-sensitive, so unpinned installs are fragile.

## Goal

`requirements.txt` pins known-good versions for every dependency, the trailing
whitespace is gone, and a single Python version is used consistently across the
repo.

## Implementation steps

1. In a clean environment matching the target Python version, install the
   packages, verify the notebook and app run, then freeze exact versions:
   ```bash
   pip freeze > requirements.lock.txt
   ```
   and pin `requirements.txt` to the resolved versions (either compatible
   `~=`/`==` pins or the full lock).
2. Ensure every import used is listed: `pandas`, `numpy`, `nltk`,
   `scikit-learn`, `tensorflow`, `streamlit` (and `gensim` if Issue 12 (#TBD) is
   done). Remove the trailing space after `tensorflow`.
3. Reconcile the Python version to one value (recommend `3.11`) across
   `.python-version`, `README.md` (Issue 04 (#TBD)), and the notebook kernel.
4. Confirm a fresh `pip install -r requirements.txt` succeeds on that Python
   version and the notebook/app still run.

## Affected files

- `requirements.txt`
- `.python-version`
- `README.md`

## Acceptance criteria

- [ ] Every dependency in `requirements.txt` has a version constraint.
- [ ] No trailing whitespace or stray blank entries remain.
- [ ] Every third-party import in the code is present in `requirements.txt`.
- [ ] A single Python version is stated consistently in `.python-version`,
      `README.md`, and the notebook kernel metadata.
- [ ] `pip install -r requirements.txt` succeeds on a clean environment.

## Dependencies

- Python-version reconciliation overlaps with Issue 04 (#TBD); add `gensim` here
  if Issue 12 (#TBD) is implemented.
