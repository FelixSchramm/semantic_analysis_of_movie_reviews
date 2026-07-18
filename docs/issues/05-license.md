# Issue 05: Add an explicit open-source LICENSE

**Priority:** P1 — A public portfolio repo with no licence leaves reviewers
unsure whether they may read, run, or reference the code. Adding one is a
standard professionalism signal.
**Affects:** new `LICENSE`

## Context

`git ls-files` shows no `LICENSE` file. Without one, the default is "all rights
reserved", which is an odd signal for a project explicitly meant to be shown off
and, ideally, reused as a reference.

## Goal

The repository carries a clear, permissive open-source licence appropriate for a
portfolio project, and the README states it.

## Implementation steps

1. Choose a permissive licence (MIT is the conventional default for portfolio
   projects).
2. Add a top-level `LICENSE` file with the standard MIT text, the correct year,
   and the author's name.
3. Add a short "License" section to the README referencing it.
4. Confirm GitHub's repository sidebar detects and displays the licence.

## Affected files

- `LICENSE` (new)
- `README.md` (License section)

## Acceptance criteria

- [ ] A `LICENSE` file exists at the repo root with valid, standard licence text.
- [ ] The copyright line has the correct year and author name.
- [ ] The README references the licence.
