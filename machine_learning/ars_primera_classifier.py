import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load your dataset (list of dicts with "content" and "tag")
with open("data/dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Handle missing values: Fill NaN values with an empty string or drop them
df = df.fillna('')  # Option 1: Fill NaN with empty string

X = df["content"]
y = df["tag"]

# Train/test split (stratified to preserve class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_df=0.9)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Linear SVM with hinge loss and balanced class weights
clf = SGDClassifier(loss="hinge", class_weight="balanced", random_state=42)
clf.fit(X_train_tfidf, y_train)

# Evaluation
y_pred = clf.predict(X_test_tfidf)
print(classification_report(y_test, y_pred, digits=3))
