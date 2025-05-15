from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import torch
import numpy as np

# Import fungsi rekomendasi dari api
from api.recommender import (
    get_top_n_recommendations,
    get_popular_books,
    get_random_books,
    get_similar_books_cf  # optional: collaborative similarity
)
from api.recommender_content import (
    recommend_similar_books as get_similar_books_content,
    search_books_by_title)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
try:
    books = pd.read_csv("data/raw/Books.csv", delimiter=",")
    ratings = pd.read_csv("data/raw/Ratings.csv", delimiter=",")
    users = pd.read_csv("data/raw/Users.csv", delimiter=",")
    print(books.info())
    ratings.columns = ratings.columns.str.strip()
    ratings = ratings[['User-ID', 'ISBN', 'Book-Rating']]
    ratings.columns = ['user_id', 'isbn', 'rating']
    # books['Year-Of-Publication'] = pd.to_numeric(books['Year-Of-Publication'], errors='coerce')
    # books = books.dropna(subset=['Year-Of-Publication'])
    # books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(int)
    # print(f"len books_new: {len(books)}")
    # print(books.info())

except Exception as e:
    print(f"Error loading data: {str(e)}")
    ratings = None
    books = None
    users = None

# --- ROUTING ---

@app.get("/")
def root():
    return {"message": "Welcome to Book Recommendation API"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/recommend/user/{user_id}")
def recommend_books(user_id: int):
    try:
        if books is None or ratings is None:
            raise HTTPException(status_code=500, detail="Data not loaded")

        recommendations = get_top_n_recommendations(user_id, ratings, books, top_n=5)
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/popular")
def get_popular():
    try:
        return {"books": get_popular_books(ratings, books)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/random")
def get_random():
    try:
        return {"books": get_random_books(books)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/similar/{isbn}")
def similar_books(isbn: str):
    try:
        similar_books = recommend_similar_books(isbn)
        match = books[books['ISBN'] == isbn]
        if match.empty:
            raise HTTPException(status_code=404, detail="Book not found")

        original_book = match.iloc[0]

        return {
            "original": {
                "isbn": isbn,
                "title": original_book['Book-Title'],
                "author": original_book['Book-Author']
            },
            "recommendations": similar_books
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search_and_recommend")
def search_and_recommend(title_query: str):
    try:
        results = search_books_by_title(title_query)
        if results.empty:
            raise HTTPException(status_code=404, detail="No matching book found")

        isbn = results.iloc[0]['ISBN']
        similar_books = recommend_similar_books(isbn)

        return {
            "original": {
                "isbn": isbn,
                "title": results.iloc[0]['Book-Title'],
                "author": results.iloc[0]['Book-Author']
            },
            "recommendations": similar_books
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/similar_content/{isbn}")
def similar_books_content(isbn: str):
    try:
        return {"similar_books": get_similar_books_content(isbn)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
def search_book_by_title(title: str):
    try:
        matches = books[books["Book-Title"].str.contains(title, case=False, na=False)]
        if matches.empty:
            raise HTTPException(status_code=404, detail="Book not found")
        top_match = matches.iloc[0]
        return {
            "ISBN": top_match["ISBN"],
            "Book-Title": top_match["Book-Title"],
            "Book-Author": top_match["Book-Author"],
            "Year-Of-Publication": top_match["Year-Of-Publication"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/newest")
def get_newest_books():
    try:
        if books is None:
            raise HTTPException(status_code=500, detail="Books data not loaded")
        
        # Sort by Year-Of-Publication descending
        newest_books = books.copy()
        newest_books["Year-Of-Publication"] = pd.to_numeric(newest_books["Year-Of-Publication"], errors="coerce")
        newest_books = newest_books.sort_values(by="Year-Of-Publication", ascending=False)
        newest_books = newest_books.head(10).fillna("")

        result = newest_books.to_dict(orient="records")
        return {"books": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))