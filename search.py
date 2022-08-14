#!/usr/bin/env python3
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


titles = pd.read_json("books_titles.json")
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(titles["mod_title"])
query = "growth of the soil"

def search(query, vectorizer, tfidf):
    processed = re.sub("[^a-zA-Z0-9 ]", "", query.lower())
    query_vec = vectorizer.transform([processed])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    results = titles.iloc[indices]
    results = results.sort_values("ratings", ascending=False)

    return results

results = search(query, vectorizer, tfidf)
print(results)
