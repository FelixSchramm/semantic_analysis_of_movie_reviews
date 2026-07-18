# Issue 12: Use `gensim` and add intrinsic evaluation + visualization

**Priority:** P2 — This is the depth/differentiation layer. The hand-rolled Keras
CBOW works but produces no evidence of embedding quality, so the README's
similarity/analogy claims (Issue 04 (#TBD)) are untested. Standard tooling plus a
simple evaluation is what makes the project convincing rather than just runnable.
**Affects:** `code.ipynb`, `src/train.py`, `README.md`, `requirements.txt`

## Context

- `create_cbow_data` (cell 07) + a Keras `Sequential` softmax over the full
  vocab (cell 09) reimplement, slowly and without evaluation, what
  `gensim.models.Word2Vec` does in a few lines with well-tested defaults.
- No embedding-quality metric or visualization is produced anywhere, so nothing
  substantiates the "semantic relationships" and analogy claims in the README.

## Goal

The project either adopts `gensim.models.Word2Vec` (recommended) or keeps the
Keras model but adds a proper intrinsic evaluation and a visualization, so the
README's claims are backed by numbers and a figure.

## Implementation steps

1. **Preferred — adopt gensim** for the model:
   ```python
   from gensim.models import Word2Vec
   model = Word2Vec(sentences=tokenized_reviews, vector_size=300,
                    window=5, min_count=5, sg=0, workers=4, epochs=20)
   ```
   `model.wv.most_similar("good")` and
   `model.wv.evaluate_word_analogies(...)` then replace the manual cosine and
   analogy code, and the app can query `model.wv` directly.
2. Add an intrinsic evaluation cell/function:
   - analogy accuracy via `KeyedVectors.evaluate_word_analogies` against the
     standard `questions-words.txt` set (note: many entries will be OOV for a
     movie-review vocab — report coverage alongside accuracy), and/or
   - a small curated similarity sanity check (e.g. nearest neighbours of
     `movie`, `good`, `actor`).
3. Add an embedding visualization: project a sample of the most frequent
   vectors to 2-D with `sklearn.manifold.TSNE` (or PCA) and plot. **Run t-SNE on
   a sample of only a few thousand vectors, not the full vocabulary**, to keep it
   fast.
4. Record the resulting numbers/figure and feed them into the README claims
   (Issue 04 (#TBD)); if the model is switched to gensim, update the app
   (Issue 03 (#TBD)) and artifacts (Issue 02 (#TBD)) accordingly.
5. Add `gensim` to `requirements.txt` (Issue 09 (#TBD)).

## Affected files

- `code.ipynb`
- `src/train.py` (if using `src/` from Issue 10 (#TBD))
- `README.md`
- `requirements.txt`

## Acceptance criteria

- [ ] The notebook produces at least one quantitative embedding-quality signal
      (analogy accuracy with coverage, or a documented similarity sanity check).
- [ ] An embedding visualization (t-SNE/PCA on a bounded sample) is produced.
- [ ] If gensim is adopted, the app and artifacts are updated to match, and
      `gensim` is pinned in `requirements.txt`.
- [ ] The README's capability claims reference this evidence.

## Dependencies

- Builds on Issue 10 (#TBD) (where to put training code); feeds Issue 04 (#TBD)
  (README claims). If gensim replaces Keras, revisit Issue 02 (#TBD) and
  Issue 03 (#TBD).
