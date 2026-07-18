# Issue 08: Stop committing the 32 MB dataset as a raw git blob

**Priority:** P1 — A 32 MB CSV committed directly bloats every clone forever and
directly contradicts the README's "Git LFS" claim. Reviewers who inspect the repo
history will see the mismatch.
**Affects:** `MovieReview.csv`, `README.md`, new `.gitattributes` or a download
script

## Context

- `git cat-file -s HEAD:MovieReview.csv` returns `32,950,157` bytes and the file
  is a plain blob, not an LFS pointer (`git-lfs` string absent from its header).
- `README.md:24` claims "Git LFS for large file storage", but there is no
  `.gitattributes` and LFS is not initialised.
- The file already sits in history, so simply deleting it now does not reclaim
  clone size unless history is rewritten.

## Goal

The large dataset is handled in one consistent, documented way — Git LFS, or an
external download — and the README's claim matches the implementation. New clones
are not forced to pull tens of MB of raw CSV through normal git objects.

## Implementation steps

Pick **one** approach and apply it consistently:

- **Option A — Git LFS (keeps the dataset in-repo):**
  1. `git lfs install && git lfs track "*.csv"`; commit `.gitattributes`.
  2. Migrate existing history so the blob is stored in LFS:
     `git lfs migrate import --include="*.csv" --everything` (note: rewrites
     history; coordinate before pushing to a shared branch).
  3. Keep the README's LFS claim.

- **Option B — External download (keeps the repo small):**
  1. Remove `MovieReview.csv` from tracking and add it to `.gitignore`
     (Issue 06 (#TBD)); optionally purge it from history with
     `git filter-repo`.
  2. Add a small `scripts/download_data.py` (or a documented URL) that fetches
     the dataset to the repo root using the correct filename.
  3. Remove the "Git LFS" claim from the README (Issue 04 (#TBD)) and document
     the download step in "How to run" (Issue 07 (#TBD)).

## Affected files

- `MovieReview.csv`
- `.gitattributes` (Option A) **or** `scripts/download_data.py` (Option B)
- `.gitignore` (Option B)
- `README.md`

## Acceptance criteria

- [ ] The dataset is handled by exactly one documented mechanism (LFS or
      external download), with no leftover contradiction.
- [ ] The README's statement about the dataset matches the chosen mechanism.
- [ ] A fresh clone either pulls the CSV via LFS or has a one-command way to
      obtain it, using the filename `MovieReview.csv`.

## Dependencies

- Coordinates with Issue 02 (#TBD) (artifact distribution), Issue 04 (#TBD)
  (README claim), Issue 06 (#TBD) (gitignore), and Issue 07 (#TBD) (run steps).
