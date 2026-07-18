# Issue 13: Remove course artifacts, debug leftovers, and interactive downloads

**Priority:** P3 — Polish. Individually minor, but course-exercise comments,
debug leftovers, a leaked local path, and interactive downloads collectively make
the repo read like an unfinished assignment rather than a portfolio piece.
**Affects:** `app.py`, `code.ipynb`, general repo hygiene

## Context

Concrete leftovers observed:

- Root `app.py` carries DataScientest checklist comments `# (a)` … `# (j)` and a
  trailing `df.head()` (`app.py:53`) — course-exercise scaffolding. (Most of this
  is removed by Issue 03 (#TBD) when `app.py` is replaced; this issue is the
  sweep for anything left.)
- Interactive `nltk.download()` (no args) appears in the code and blocks
  execution (also addressed for the notebook in Issue 01 (#TBD)); ensure no such
  call remains anywhere.
- The notebook's cell 02 output leaks a local path `/Users/felix/nltk_data`
  (re-running cleanly per Issue 01 (#TBD) removes it; confirm it is gone).
- Git history messages are terse and non-descriptive (`Code Update`, three ×
  `Update README.md`). Adopt clear imperative commit messages going forward.

## Goal

No course-exercise scaffolding, debug leftovers, interactive/blocking calls, or
leaked local paths remain in the tracked code or notebook outputs, and commit
hygiene improves from here on.

## Implementation steps

1. Grep the repo for leftovers and remove them: `# (a)`–`# (j)` style comments,
   stray `df.head()`/`df.info` debug lines, `display(...)` used only for
   debugging, and any `nltk.download()` without an explicit dataset argument.
2. Confirm no notebook output contains a local filesystem path (re-run per
   Issue 01 (#TBD) if needed).
3. Adopt descriptive, imperative commit messages for all future commits (this is
   a going-forward convention, not a history rewrite).
4. Optional: add a short `CONTRIBUTING`/commit-style note if desired.

## Affected files

- `app.py`
- `code.ipynb`
- Repo conventions (commit messages)

## Acceptance criteria

- [ ] No `# (a)`–`# (j)` course-checklist comments remain in tracked code.
- [ ] No `nltk.download()` without an explicit dataset argument remains anywhere.
- [ ] No tracked notebook output contains a local path such as
      `/Users/<name>/...`.
- [ ] No stray debug lines (`df.head()`/`df.info`) remain outside intentional,
      explained usage.

## Dependencies

- Overlaps with Issue 01 (#TBD) (notebook re-run) and Issue 03 (#TBD) (app
  replacement); this issue is the final sweep for anything those leave behind.
