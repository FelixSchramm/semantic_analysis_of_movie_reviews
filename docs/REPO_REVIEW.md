# Repository Review — Semantic Analysis of Movie Reviews

## Purpose of this document

This is a portfolio project intended to be shown to recruiters and interviewers
(Data Science / Machine Learning). This review answers one question:

> *"Is this repository, as it stands, something you can put in front of an
> interviewer — and what would an experienced reviewer criticise about it?"*

Every finding below was verified directly against the repository (specific file,
notebook cell, or line). No claim is included without evidence.

- **Reviewed commit:** `2f07521` (`Update README.md`)
- **Reviewed branch:** `main`
- **Tracked files:** `.python-version`, `MovieReview.csv`, `README.md`, `app.py`,
  `code.ipynb`, `requirements.txt`

The briefings referenced below live (temporarily) under `docs/issues/` and are
being migrated into the GitHub issue tracker. See the *Lifecycle* note at the end.

---

## Strengths

A fair review names what is good, not only what is broken:

- **The concept is well chosen and recruiter-legible.** A Word2Vec (CBOW)
  embedding model with an interactive similarity/analogy demo is a clean,
  self-contained NLP story that an interviewer can grasp in seconds.
- **The README is well written and structured** — summary, core functionality,
  tech stack, data source, and attribution are all present and clearly phrased
  (`README.md`).
- **The "clean" notebook (`code.ipynb`) is nicely narrated** with sectioned
  markdown headers and a readable CBOW implementation
  (`create_cbow_data`, cell 07).
- **The Streamlit app idea is genuinely nice UX** — top-10 cosine-similar words
  plus vector analogies (`king − man + woman`) in the notebook's `app.py` cell
  (cell 12).
- **No misleading metrics are reported.** Because the model is unsupervised, the
  README does not quote an inflated accuracy/AUC — a trap this project avoids.
  (The credibility risk here is different; see P0 below.)

---

## Note on "data leakage / implausible metrics"

Classic supervised label leakage does **not** apply here: the task is
unsupervised word-embedding learning, the `sentiment` column is dropped before
training (`code.ipynb` cell 02, `app.py:19`), and no held-out metric is quoted.
That is a point in the project's favour.

The equivalent credibility risk for *this* project is different and real:

1. a notebook that was **never run end-to-end** and ships a broken cell plus an
   error traceback (P0 — Issue 01),
2. a checked-in `app.py` that is **not the app the README describes** (P0 —
   Issue 03), and
3. **README claims that the repository does not back up** — a live demo `LINK`
   placeholder, a Git-LFS claim with no LFS, and strong "semantic analogy"
   capability claims that a tiny 5-epoch CBOW is unlikely to demonstrate
   (P0 — Issue 04; P2 — Issue 12).

An interviewer who opens the notebook or tries to run the app will hit these
within a minute. They are the things to fix before the repo is shown.

---

## Findings by severity

Priorities: **P0** credibility (fix before any application) · **P1**
structure/professionalism · **P2** domain depth/differentiation · **P3** polish.

### P0 — Credibility

| # | Finding | Evidence |
|---|---------|----------|
| 01 | Notebook was never "Restart & Run All"; ships a syntax error and a committed error traceback. | Only cell 02 has `execution_count=10`; all other code cells are `None` (non-monotone). Cell 03 source ends with `3df.head()` (syntax error). Cell 03 calls interactive `nltk.download()` (no args) and its saved output is a `KeyboardInterrupt` error. |
| 02 | The trained model artifact is missing and unreproducible from a fixed pipeline. | `git ls-files` has no `word2vec.h5`; `app.py` / notebook `load_model('word2vec.h5')` would fail. Training epochs differ across files (notebook cell 10 = 5; the old script implied 50). |
| 03 | The checked-in `app.py` is a course training script, not the Streamlit app the README advertises — and the real app (notebook cell 12) has runtime bugs. | Root `app.py` imports `streamlit as st` but never calls it; it contains DataScientest checklist comments `# (a)`–`# (j)`, an interactive `nltk.download()` (`app.py:29`), and a trailing `df.head()` (`app.py:53`). The notebook's `app.py` uses `pd.read_csv` with **no `import pandas`** and re-fits a tokenizer on **raw** (un-preprocessed) reviews, so its indices do not match the model trained on preprocessed text (train/serve skew). |
| 04 | README makes claims the repo does not support. | `README.md:11` demo link is literally `LINK`; `README.md:24` claims "Git LFS" but there is no `.gitattributes` and `MovieReview.csv` is a raw 32 MB blob; `README.md:20` says "Python 3.8+" while `.python-version` is `3.11.9` and the notebook kernel is `3.9.6`; the analogy capability claim (`README.md:16`) is unsubstantiated. |

### P1 — Structure / professionalism

| # | Finding | Evidence |
|---|---------|----------|
| 05 | No `LICENSE`. | Not in `git ls-files`; a public portfolio repo without a licence is ambiguous to reviewers. |
| 06 | No `.gitignore`. | Not in `git ls-files`; artifacts (`word2vec.h5`, `__pycache__/`, `nltk_data/`, `.DS_Store`) can be committed by accident. |
| 07 | No "How to run" instructions. | `README.md` has no setup/data-download/train/launch section; the data-source link (`README.md:28`) points at a course S3 URL with a different filename than the repo's `MovieReview.csv`. |
| 08 | A 32 MB dataset is committed raw into git. | `git cat-file -s HEAD:MovieReview.csv` = 32,950,157 bytes; not an LFS pointer. Bloats every clone and contradicts the LFS claim. |
| 09 | Unpinned dependencies; inconsistent Python version. | `requirements.txt` lists bare names with a trailing space after `tensorflow`; no versions. Python version disagreement (see Issue 04). |
| 10 | Logic lives only in notebook cells / a monolithic script; nothing importable or testable. | Preprocessing + CBOW + training exist only inside `code.ipynb` and the root `app.py`; no `src/` package. |
| 11 | No tests, no CI. | No `tests/`, no `.github/workflows/`; nothing guards the preprocessing/CBOW logic or lints the code. |

### P2 — Domain depth / differentiation

| # | Finding | Evidence |
|---|---------|----------|
| 12 | Hand-rolled Keras CBOW with no evaluation; standard tooling (`gensim`) and intrinsic evaluation are missing. | `create_cbow_data` (cell 07) + Keras `Sequential` (cell 09) reimplement what `gensim.models.Word2Vec` does in a few lines with `most_similar` / `evaluate_word_analogies`. No embedding quality metric or visualization is produced, so the README's semantic claims are untested. |

### P3 — Polish

| # | Finding | Evidence |
|---|---------|----------|
| 13 | Course-exercise artifacts, debug leftovers, interactive downloads, and a leaked local path. | `# (a)`–`# (j)` comments and `df.head()` in root `app.py`; interactive `nltk.download()`; cell 02 output leaks `/Users/felix/nltk_data`; git history messages are terse (`Code Update`, three × `Update README.md`). |

---

## Prioritised list → briefings

> These links point at the working briefings under `docs/issues/`. After the
> issues are opened on GitHub, this table is updated to point at the tracker
> (see Lifecycle note).

| Priority | Briefing | Title |
|----------|----------|-------|
| P0 | [`01-notebook-reproducibility.md`](issues/01-notebook-reproducibility.md) | Fix broken notebook cells and re-execute end-to-end |
| P0 | [`02-training-artifacts.md`](issues/02-training-artifacts.md) | Make the trained model and tokenizer reproducible and available |
| P0 | [`03-streamlit-app.md`](issues/03-streamlit-app.md) | Ship the real Streamlit app as `app.py` and fix its runtime bugs |
| P0 | [`04-readme-truthfulness.md`](issues/04-readme-truthfulness.md) | Align the README with what the repository actually contains |
| P1 | [`05-license.md`](issues/05-license.md) | Add an explicit open-source LICENSE |
| P1 | [`06-gitignore.md`](issues/06-gitignore.md) | Add a `.gitignore` for Python / ML artifacts |
| P1 | [`07-how-to-run.md`](issues/07-how-to-run.md) | Add reproducible "How to run" instructions |
| P1 | [`08-dataset-handling.md`](issues/08-dataset-handling.md) | Stop committing the 32 MB dataset as a raw git blob |
| P1 | [`09-pin-dependencies.md`](issues/09-pin-dependencies.md) | Pin dependencies and align the Python version |
| P1 | [`10-modularize-src.md`](issues/10-modularize-src.md) | Extract an importable `src/` package |
| P1 | [`11-tests-ci.md`](issues/11-tests-ci.md) | Add tests and CI (ruff + pytest on synthetic data) |
| P2 | [`12-gensim-evaluation.md`](issues/12-gensim-evaluation.md) | Use `gensim` and add intrinsic evaluation + visualization |
| P3 | [`13-polish.md`](issues/13-polish.md) | Remove course artifacts, debug leftovers, and interactive downloads |

**Suggested order of attack:** 01 → 02 → 03 → 04 (the P0 credibility chain),
then the P1 hygiene items (05–11), then 12 (depth), then 13 (polish).

---

## Lifecycle of this document

`docs/REPO_REVIEW.md` is temporary working material. The individual briefings
have been migrated to the GitHub issue tracker; this file remains only as a
prioritised overview linking to those issues. **Once the P0 and P1 items are
resolved, delete this document as well** — a finished portfolio repository
should present the polished result, not its own review scaffolding.
