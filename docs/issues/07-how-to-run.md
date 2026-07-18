# Issue 07: Add reproducible "How to run" instructions

**Priority:** P1 — There is no way for a reviewer to go from `git clone` to a
running demo. A portfolio project that cannot be reproduced in a few documented
steps loses most of its value.
**Affects:** `README.md`

## Context

`README.md` has a "Technical Stack" and "Data Source" section but no
setup/run instructions. The data-source link (`README.md:28`) points at a course
S3 URL for `Movie Review.csv` (note the space) while the repo file is
`MovieReview.csv`, so even obtaining the data is ambiguous. There is no mention
of creating an environment, installing dependencies, obtaining/downloading NLTK
data, training the model, or launching the app.

## Goal

The README contains a copy-pasteable "How to run" section that takes a reviewer
from a fresh clone to (a) a reproduced notebook run and (b) a running Streamlit
app, with the data-acquisition step explicit and correct.

## Implementation steps

1. Add a "Getting Started" / "How to run" section to the README with numbered
   steps:
   1. Create and activate a virtual environment (state the Python version from
      Issue 04 (#TBD)).
   2. `pip install -r requirements.txt` (pinned via Issue 09 (#TBD)).
   3. Obtain the dataset: describe exactly how `MovieReview.csv` is acquired
      (LFS pull, download script, or Release asset — see Issue 08 (#TBD)), using
      the correct filename.
   4. Download NLTK data non-interactively (e.g.
      `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"`).
   5. Train / obtain the model (Issue 02 (#TBD)): either run the training entry
      point or download the released artifacts.
   6. Launch the app: `streamlit run app.py`.
2. Keep every command runnable as written on a clean machine; test them yourself.
3. Cross-link this section from the "Interactive Demonstration" area if the live
   link is removed in Issue 04 (#TBD).

## Affected files

- `README.md`

## Acceptance criteria

- [ ] The README has a clearly headed "How to run" (or "Getting Started")
      section with numbered, copy-pasteable commands.
- [ ] The data-acquisition step names the correct file (`MovieReview.csv`) and a
      working method to obtain it.
- [ ] NLTK data download is shown non-interactively (explicit dataset names).
- [ ] The steps, followed on a clean clone, end in a running `streamlit run app.py`.

## Dependencies

- References Issue 02 (#TBD) (model), Issue 08 (#TBD) (data acquisition), and
  Issue 09 (#TBD) (pinned deps).
