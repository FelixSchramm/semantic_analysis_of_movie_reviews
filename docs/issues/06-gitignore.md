# Issue 06: Add a `.gitignore` for Python / ML artifacts

**Priority:** P1 — With no `.gitignore`, build and runtime artifacts can be
committed by accident (the missing-then-present `word2vec.h5`, `__pycache__/`,
downloaded `nltk_data/`, `.DS_Store`). This is basic repo hygiene reviewers
notice.
**Affects:** new `.gitignore`

## Context

`git ls-files` shows no `.gitignore`. The project generates a model artifact, may
download NLTK corpora locally, and is developed on macOS (the notebook output
leaks `/Users/felix/nltk_data`, implying `.DS_Store` risk). None of these should
enter version control.

## Goal

A `.gitignore` prevents common Python, Jupyter, ML-artifact, and OS files from
being committed, while still allowing intentionally tracked artifacts (if Git LFS
is chosen in Issue 02 (#TBD) / Issue 08 (#TBD)).

## Implementation steps

1. Add a `.gitignore` at the repo root covering at least:
   - Python: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `*.egg-info/`
   - Jupyter: `.ipynb_checkpoints/`
   - ML artifacts: `word2vec.h5`, `word2vec.keras`, `tokenizer.pkl`
     (unless tracked via LFS in Issue 02 (#TBD))
   - Data cache: `nltk_data/`
   - OS: `.DS_Store`, `Thumbs.db`
2. If Git LFS is chosen for the model artifacts, ensure the ignore rules and the
   LFS `track` rules do not conflict.
3. Verify nothing currently tracked is newly ignored in a way that removes it;
   `git status` should stay clean.

## Affected files

- `.gitignore` (new)

## Acceptance criteria

- [ ] A `.gitignore` exists at the repo root.
- [ ] It ignores `__pycache__/`, `.ipynb_checkpoints/`, `.DS_Store`,
      `nltk_data/`, and virtual-env directories.
- [ ] Model artifacts are ignored unless explicitly tracked via Git LFS.
- [ ] `git status` on a clean checkout reports no unexpected changes.

## Dependencies

- Coordinate the model-artifact rules with Issue 02 (#TBD) and Issue 08 (#TBD).
