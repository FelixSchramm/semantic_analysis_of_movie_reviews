# Contributing

A few conventions keep this repository portfolio-ready.

## Commit messages

- Write in the imperative mood ("Add training script", not "Added" / "Code update").
- Summarise *what* and *why* in the subject line; add a body when the change
  needs context.

## Code hygiene

- Keep the code free of course-exercise scaffolding: no lettered checklist
  comments (`# (a)`, `# (b)`, …) and no leftover debug lines (`df.head()`,
  `df.info`) outside intentional, explained use.
- Download NLTK data non-interactively with explicit resource names
  (`nltk.download("stopwords")`), never a bare `nltk.download()` that opens the
  interactive downloader.
- Reuse the shared preprocessing in `src/` rather than re-implementing it, so
  training and serving stay consistent.

## Before committing

- Run the linter and tests:
  ```bash
  ruff check .
  pytest -q
  ```
- Re-execute notebooks so their outputs are current and their execution counts
  are monotonic:
  ```bash
  jupyter nbconvert --to notebook --execute --inplace code.ipynb
  ```
- Do not commit generated artifacts (trained models, `__pycache__`, downloaded
  NLTK data); these are covered by `.gitignore`.
