# Issue 04: Align the README with what the repository actually contains

**Priority:** P0 — A public portfolio README that states things the repo does not
back up (a live demo that is a `LINK` placeholder, "Git LFS" that isn't used,
capabilities that aren't demonstrated) reads as careless or misleading to a
recruiter. Truthfulness is a credibility issue, not polish.
**Affects:** `README.md`, `.python-version`

## Context

Line-by-line, the README diverges from the repo:

- `README.md:11` — the "live version" link is the literal text `LINK`.
- `README.md:24` — claims "Git LFS for large file storage", but there is no
  `.gitattributes` and `MovieReview.csv` is a raw 32 MB blob (see Issue 08 (#TBD)).
- `README.md:20` — states "Python 3.8+", while `.python-version` pins `3.11.9`
  and the notebook kernel metadata says `3.9.6`.
- `README.md:16` — claims the model demonstrates analogies such as
  `king − man + woman`. A 5-epoch Keras CBOW over 25k reviews (vocab 10k) is
  unlikely to show this reliably; the claim is currently unsubstantiated (see
  Issue 12 (#TBD)).
- `README.md:28` — the data-source link points at a course S3 URL for
  `Movie Review.csv`, while the repo file is `MovieReview.csv`; the link may be
  unreachable to outsiders.

## Goal

Every factual claim in the README is either true of the repository as committed
or removed/softened. A reader can trust the README as an accurate map of the
project.

## Implementation steps

1. Replace the `LINK` placeholder with the real deployed Streamlit URL, or, if
   there is no live deployment, remove the "Interactive Demonstration" section
   and instead point to the "How to run" instructions (Issue 07 (#TBD)).
2. Make the Git-LFS statement match reality: either implement LFS (Issue 08 (#TBD))
   and keep the claim, or remove the claim.
3. Reconcile the Python version to a single value across `README.md`,
   `.python-version`, and the notebook kernel (recommend `3.11`).
4. Soften or substantiate the capability claims: describe what the model does
   (nearest-neighbour similarity, vector arithmetic) without overstating analogy
   performance until Issue 12 (#TBD) provides evidence; if evaluation numbers
   exist, quote them.
5. Fix the data-source section so the filename matches (`MovieReview.csv`) and
   the acquisition path actually works for an outside reader (coordinate with
   Issue 07 (#TBD) and Issue 08 (#TBD)).

## Affected files

- `README.md`
- `.python-version` (only if the reconciled version differs)

## Acceptance criteria

- [ ] The README contains no placeholder text such as `LINK`.
- [ ] The Git-LFS statement is true of the repo, or is removed.
- [ ] A single Python version is stated consistently in `README.md`,
      `.python-version`, and the notebook kernel metadata.
- [ ] Capability claims are either backed by evidence (Issue 12 (#TBD)) or worded
      so they do not overstate what the model demonstrably does.
- [ ] The data-source filename/link matches the repo and is reachable, or the
      section explains exactly how to obtain the data.

## Dependencies

- Best done after Issue 03 (#TBD) (real demo/app), Issue 07 (#TBD) (run
  instructions), Issue 08 (#TBD) (LFS decision), and informed by Issue 12 (#TBD)
  (evaluation) — but the placeholder and version fixes can land immediately.
