# Issue 01: Fix broken notebook cells and re-execute end-to-end

**Priority:** P0 — A committed notebook that does not run, contains a syntax
error, and ships an error traceback is the first thing an interviewer opens; it
undermines the credibility of everything else in the repo.
**Affects:** `code.ipynb`

## Context

`code.ipynb` was never run cleanly from top to bottom before being committed:

- Execution counts are non-monotone. Only cell 02 has
  `execution_count = 10`; every other code cell has `execution_count = null`.
  This means "Restart & Run All" was never performed.
- Cell 03 ends with the line `3df.head()` — a stray leading `3` makes this a
  **syntax error**, so the cell cannot run as written.
- Cell 03 calls `nltk.download()` with **no arguments**, which opens NLTK's
  interactive downloader and blocks. The saved output of that cell is a
  `KeyboardInterrupt` error traceback, committed into the notebook.
- Cell 03 duplicates the preprocessing already present earlier and is not needed
  in the clean pipeline.

## Goal

`code.ipynb` runs top to bottom without errors in a fresh kernel, has strictly
increasing execution counts, contains no committed error output, and no
interactive/blocking calls. Opening the notebook shows a clean, coherent run.

## Implementation steps

1. Fix the broken cell 03: remove the stray `3` typo (`3df.head()` →
   `df.head()`), or delete cell 03 entirely if it duplicates the preprocessing
   already defined in an earlier cell (it does — consolidate to one
   preprocessing cell).
2. Replace every interactive `nltk.download()` with targeted, non-interactive
   downloads: `nltk.download('stopwords')`, `nltk.download('punkt')`, and
   `nltk.download('punkt_tab')` (the last is required by newer NLTK for
   `word_tokenize`). Wrap them so they are quiet on re-run.
3. Ensure the notebook does not require the full 32 MB dataset to be re-trained
   for a clean run to succeed. Either keep training epochs small and clearly
   labelled as a demo, or read the number of epochs from a variable defined once
   at the top.
4. From the repo root, perform a scriptable "Restart & Run All":
   ```bash
   jupyter nbconvert --to notebook --execute --inplace code.ipynb
   ```
   Fix any error surfaced until the command exits 0.
5. Confirm the resulting notebook has monotonically increasing
   `execution_count` values and no `output_type: error` cells.

## Affected files

- `code.ipynb`

## Acceptance criteria

- [ ] `jupyter nbconvert --to notebook --execute --inplace code.ipynb` exits 0.
- [ ] All code cells have strictly increasing, non-null `execution_count` values.
- [ ] No cell contains an `output_type: "error"` output.
- [ ] The notebook contains no `nltk.download()` call without an explicit
      dataset argument.
- [ ] The string `3df.head()` no longer appears anywhere in `code.ipynb`.
