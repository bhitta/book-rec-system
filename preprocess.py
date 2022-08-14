#!/usr/bin/env python3
import gzip
import json
import pandas as pd

def parse_fields(line) -> dict:

    data = json.loads(line)
    return {
        "book_idk": data["book_id"],
        "title": data["title_without_series"],
        "ratings": data["ratings_count"],
        "url": data["url"],
        "cover_image": data["image_url"]
        }

def return_title_dict(gz_path: str) -> dict:

    books_titles = []
    with gzip.open(gz_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            fields = parse_fields(line)

            try:
                ratings = int(fields["ratings"])
            except ValueError:
                continue
            if ratings > 15:
                books_titles.append(fields)

    return books_titles

def preprocess_book_titles(books_titles: dict) -> dict:

    titles = pd.DataFrame.from_dict(books_titles)
    titles["ratings"] = pd.to_numeric(titles["ratings"])
    titles["mod_title"] = titles["title"].str.replace("[^a-zA-Z0-9 ]", "", regex=True)
    titles["mod_title"] = titles["mod_title"].str.lower()
    titles["mod_title"] = titles["mod_title"].str.replace("\s+", " ", regex=True)
    titles = titles[titles["mod_title"].str.len() > 0]

    return titles

if __name__ == "__main__":
    books_titles = return_title_dict("goodreads_books.json.gz")
    preprocessed = preprocess_book_titles(books_titles)
    preprocessed.to_json("books_titles.json")
