# -*- coding: utf-8 -*-
"""Sentiment Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WbQiBuepVthf_tASyOBNgv7-PoRAF0cO
"""

import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix, accuracy_score

review_dataset = pd.read_csv('/content/drive/MyDrive/ML datasets/Sentiment Analysis/a1_RestaurantReviews_HistoricDump.tsv', delimiter = '\t', quoting = 3)

review_dataset.head()

review_dataset.shape

"""## Data Preprocessing"""

import nltk
nltk.download('stopwords')

review_dataset.isnull().sum()

"""## Now time for stemming"""

port_stem = PorterStemmer()

def Stemming(content):
  review = re.sub('[^a-zA-Z]', ' ', content)
  review = review.lower()
  review = review.split()
  review = [port_stem.stem(word) for word in review if not word in stopwords.words('english')]
  review = ' '.join(review)
  return review

review_dataset['Review'] = review_dataset['Review'].apply(Stemming)

print(review_dataset)

"""## Data Transformation

Now we will convert our cleaned dataset into bag of words representation
"""

count_vectorizer = CountVectorizer(max_features = 1420)

encoder = OneHotEncoder()

x = count_vectorizer.fit_transform(review_dataset['Review']).toarray() #this is important cause it converts the words into numerical values
y = review_dataset.iloc[:, -1].values

print(y)

# Saving Bag of words dictionary to later use in prediction
import pickle
bow_path = '/content/drive/MyDrive/ML datasets/Sentiment Analysis/c1_BoW_Sentiment_Model.pkl'
pickle.dump(count_vectorizer, open(bow_path, 'wb'))

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.20, random_state = 0)

"""# Model Fitting"""

y_train.shape

classifier = GaussianNB()
classifier.fit(x_train, y_train)

# Exporting NB Classifier to later use in prediction
import joblib
joblib.dump(classifier, 'c2_Classifier_Sentiment_Model')

pred = classifier.predict(x_test)
cm = confusion_matrix(y_test, pred)
print(cm)
accuracy = accuracy_score(y_test, pred)
print(accuracy)

