# Word2Vec Model for Semantic Analysis of Movie Reviews

## Project Summary

This project implements a Word2Vec (Continuous Bag-of-Words) model to generate word embeddings from a corpus of 25,000 movie reviews. The resulting model is exposed through an interactive web application developed with Streamlit, allowing for the exploration of semantic relationships between words.

## Interactive Demonstration

A live version of the application can be accessed here:

[Link to your deployed Streamlit App]

## Core Functionality

* **Semantic Similarity**: Users can input a word to retrieve a ranked list of the 10 most semantically similar words, calculated using cosine similarity on their vector representations.
* **Vector-based Analogies**: The application supports word arithmetic to solve analogies (e.g., `king - man + woman`), demonstrating the model's grasp of complex semantic relationships.

## Technical Stack

* **Language**: Python 3.8+
* **Machine Learning**: TensorFlow, Keras, Scikit-learn
* **Data Handling**: Pandas, NLTK
* **Web Framework**: Streamlit
* **Version Control**: Git, Git LFS for large file storage

## Data Source

The model was trained on the [Movie Review Dataset](https://train-exo.s3.eu-west-1.amazonaws.com/2317/Movie%20Review.csv), which contains 25,000 movie reviews with sentiment labels.

## Local Deployment

To run the application locally, please follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Install Git LFS and Retrieve Model**
    This project utilizes Git LFS for the model file.
    ```bash
    git lfs install
    git lfs pull
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Application**
    ```bash
    streamlit run app.py
    ```

## Repository Structure


.
├── app.py              # Main Streamlit application script
├── word2vec.h5         # Pre-trained Keras Word2Vec model
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation


## Acknowledgements

This project was developed based on the "Bonus: Deep Learning" module provided by DataScientest.
