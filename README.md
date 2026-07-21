# Word2Vec Model for Semantic Analysis of Movie Reviews

## Project Summary

This project implements a Word2Vec (Continuous Bag-of-Words) model to generate word embeddings from a corpus of 25,000 movie reviews. The resulting model is exposed through an interactive web application developed with Streamlit, allowing for the exploration of semantic relationships between words.

## Interactive Demonstration

The Streamlit application runs locally — see [Getting Started](#getting-started).
A hosted demo link will be added here once the app is deployed.

## Core Functionality

* **Semantic Similarity**: Users can input a word to retrieve a ranked list of the 10 most semantically similar words, calculated using cosine similarity on their vector representations.
* **Vector-based Analogies**: The application supports word arithmetic to explore analogies (e.g., `king - man + woman`). On this 25,000-review corpus the embeddings reach roughly 80% top-5 accuracy on a small curated analogy set — see the evaluation section of `code.ipynb` for the reproducible numbers and a t-SNE visualization.

## Technical Stack

* **Language**: Python 3.11
* **Machine Learning**: gensim (Word2Vec), Scikit-learn
* **Data Handling**: Pandas, NLTK
* **Web Framework**: Streamlit
* **Version Control**: Git (dataset hosted as a release asset — see Getting Started)

## Getting Started

These steps take you from a fresh clone to a running demo.

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FelixSchramm/semantic_analysis_of_movie_reviews.git
   cd semantic_analysis_of_movie_reviews
   ```
2. **Install uv and the project dependencies** (uv creates the virtual environment automatically):
   ```bash
   # install uv once: https://docs.astral.sh/uv/getting-started/installation/
   uv sync
   ```
3. **Download the dataset** (hosted as a GitHub release asset):
   ```bash
   uv run python scripts/download_data.py   # fetches MovieReview.csv
   ```
4. **Download the required NLTK data (non-interactive):**
   ```bash
   uv run python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
   ```
5. **Train the model** (writes `word2vec.model` and `word2vec.wv` to the current directory):
   ```bash
   uv run python -m src.train --data MovieReview.csv --out .
   ```
6. **Launch the interactive app:**
   ```bash
   uv run streamlit run app.py
   ```

To reproduce the analysis end-to-end instead, execute the notebook:
```bash
uv run --with jupyter jupyter nbconvert --to notebook --execute --inplace code.ipynb
```

## Data Source

The model was trained on a movie review dataset of 25,000 reviews with sentiment labels. The file (`MovieReview.csv`) is not committed to the repository; run `python scripts/download_data.py` (step 3 above) to fetch it from the release asset.


This project was developed based on the "Bonus: Deep Learning" module provided by DataScientest.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
