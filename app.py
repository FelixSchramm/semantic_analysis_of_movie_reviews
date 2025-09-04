import pandas as pd
import streamlit as st
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import numpy as np


# (a) Load the data file under the name df and explore it.
#Since the Word2Vec approach only requires text, we do not need the "sentiment" column of the dataframe.

# (b) Delete the "sentiment" column from df.

df = pd.read_csv("MovieReview.csv")

print(df.head())
print(df.shape)

df = df.drop('sentiment', axis=1)

# (c) Add the following code to clean up the data and to remove stopwords.

import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download()
stop_words = stopwords.words('english')

# Converts the unicode file to ascii
def unicode_to_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

def preprocess_sentence(w):
    w = unicode_to_ascii(w.lower().strip())
    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    w = re.sub(r"([?.!,¿])", r" \1 ", w)
    w = re.sub(r'[" "]+', " ", w)
    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
    w = re.sub(r"[^a-zA-Z?.!]+", " ", w)
    w = re.sub(r'\b\w{0,2}\b', '', w)

    # remove stopword
    mots = word_tokenize(w.strip())
    mots = [mot for mot in mots if mot not in stop_words]
    return ' '.join(mots).strip()

df.review = df.review.apply(lambda x :preprocess_sentence(x))
df.head()


# (d) Define a tokenizer object using the tensorflow.keras.preprocessing.text tokenizer constructor, specifying a dictionary word limit of 10000.
# (e) Update the tokenizer dictionary using the fit_on_texts method.

import tensorflow as tf
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000)
tokenizer.fit_on_texts(df.review)

# (f) Store the word-index matching dictionary in the word2idx variable, and the index-word matching dictionary in the idx2word variable, using the word_index attribute of the tokenizer.
# (h) Store the size of the dictionary in the vocab_size variable, using the num_words attribute of the tokenizer.

word2idx = tokenizer.word_index
idx2word = tokenizer.index_word
vocab_size = tokenizer.num_words

# ____________________ MODELLING  _____________________ 
# (g) Add the following code to create the data set (X, Y).



import numpy as np


def sentenceToData(tokens, WINDOW_SIZE):
    window = np.concatenate((np.arange(-WINDOW_SIZE,0),np.arange(1,WINDOW_SIZE+1)))
    X,Y=([],[])
    for word_index, word in enumerate(tokens) :
        if ((word_index - WINDOW_SIZE >= 0) and (word_index + WINDOW_SIZE <= len(tokens) - 1)) :
            X.append(word)
            Y.append([tokens[word_index-i] for i in window])
    return X, Y


WINDOW_SIZE = 5

X, Y = ([], [])
for review in df.review:
    for sentence in review.split("."):
        word_list = tokenizer.texts_to_sequences([sentence])[0]
        if len(word_list) >= WINDOW_SIZE:
            Y1, X1 = sentenceToData(word_list, WINDOW_SIZE//2)
            X.extend(X1)
            Y.extend(Y1)
    
X = np.array(X).astype(int)
y = np.array(Y).astype(int).reshape([-1,1])




# (h) Create the model architecture. The Embedding layer will take an input of size 10000 and an output of size 300. The Dense layer will consist of 10000 neurons and a SoftMax activation function.


from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, Dense, GlobalAveragePooling1D

embedding_dim = 300
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(GlobalAveragePooling1D())
model.add(Dense(vocab_size, activation='softmax'))



# (i) Compile the model.
# (j) Train the model during 50 epochs.

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, batch_size = 128, epochs=50)


# g) Save the model in H5 format using the save method in Keras.

model.save("word2vec.h5") 