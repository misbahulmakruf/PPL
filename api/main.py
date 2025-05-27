from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from api import assistant
from dotenv import load_dotenv
from fastapi import Query

# Import fungsi rekomendasi dari api
from api.recommender import (
    get_top_n_recommendations,
    get_popular_books,
    get_random_books,
    get_similar_books_cf  # optional: collaborative similarity
)
from api.recommender_content import (
    recommend_similar_books,
    search_books_by_title)

load_dotenv()
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
    books = pd.read_csv("data/processed/books_cleaned.csv", delimiter=",")
    ratings = pd.read_csv("data/processed/ratings_cleaned.csv", delimiter=",")
    users = pd.read_csv("data/raw/Users.csv", delimiter=",")
    print(books.info())
    ratings.columns = ratings.columns.str.strip()
    ratings = ratings[['User-ID', 'ISBN', 'Book-Rating']]
    ratings.columns = ['user_id', 'isbn', 'rating']
    #books['Year-Of-Publication']=int(books['Year-Of-Publication']) if str(books['Year-Of-Publication']).isdigit() else None
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
app.include_router(assistant.router)

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
        return {"books": get_random_books(books,ratings=ratings)}
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
        isbn = results.iloc[0]['ISBN']

        # Ambil data rating untuk ISBN tersebut
        book_ratings = ratings[ratings['isbn'] == isbn]

        # Hitung average rating
        if not book_ratings.empty:
            avg_rating = round(book_ratings['rating'].mean(), 2)
            count_rating = int(book_ratings['rating'].count())
        else:
            avg_rating = None
            count_rating = 0
        return {
            "original": {
                "isbn": isbn,
                "title": results.iloc[0]['Book-Title'],
                "author": results.iloc[0]['Book-Author'],
                "year":int( results.iloc[0]['Year-Of-Publication']) if str(results.iloc[0]['Year-Of-Publication']).isdigit() else None,
                "publisher": results.iloc[0]['Publisher'],
                "score": avg_rating,
                "num_ratings": count_rating

            },
            "recommendations": similar_books
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/similar_content/{isbn}")
def similar_books_content(isbn: str):
    try:
        return {"similar_books": recommend_similar_books(isbn)}
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

@app.get("/books")
def get_books(
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=500),
    query: str = ""
):
    try:
        if books is None:
            raise HTTPException(status_code=500, detail="Books data not loaded")

        filtered_books = books
        if query:
            query_lower = query.lower()
            filtered_books = books[
                books["Book-Title"].str.lower().str.contains(query_lower) |
                books["Book-Author"].str.lower().str.contains(query_lower)
            ]

        total = len(filtered_books)
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        page_data = filtered_books.iloc[start_idx:end_idx].fillna("")

        return {
            "total": total,
            "page": page,
            "size": size,
            "books": page_data.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/year_range")
def get_year_range():
    try:
        print("books:")
        print(books.head())
        if books is None:
            raise HTTPException(status_code=500, detail="Books data not loaded")
        if "Year-Of-Publication" not in books.columns:
            raise HTTPException(status_code=500, detail="Year-Of-Publication column not found")
        books_clean = books.copy()
        print("books_clean:")
        print(books_clean.head())
        if books_clean.empty:
            raise HTTPException(status_code=500, detail="No valid year data found")
        min_year = int(books_clean["Year-Of-Publication"].min())
        max_year = int(books_clean["Year-Of-Publication"].max())
        print("min_year:")
        print(min_year)
        print("max_year:")
        print(max_year)
        return {"min": min_year, "max": max_year}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        
@app.get("/books_by_year_range")
def get_books_by_year_range(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    year_start: int = Query(...),
    year_end: int = Query(...)
):
    try:
        books_filtered = books[["ISBN","Book-Title", "Book-Author", "Year-Of-Publication"]].copy()
        books_filtered["Year-Of-Publication"] = pd.to_numeric(books_filtered["Year-Of-Publication"], errors="coerce")
        filtered = books_filtered[
            (books_filtered["Year-Of-Publication"] >= year_start) &
            (books_filtered["Year-Of-Publication"] <= year_end)
        ].sort_values("Book-Title")

        total = len(filtered)
        start = (page - 1) * size
        end = start + size

        return {
            "total": total,
            "page": page,
            "books": filtered.iloc[start:end].fillna("").to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books_by_year")
def get_books_by_year(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    year: int = Query(2000)
):
    try:
        if books is None:
            raise HTTPException(status_code=500, detail="Books data not loaded")

        # Konversi tahun
        books_filtered = books.copy()
        books_filtered["Year-Of-Publication"] = pd.to_numeric(books_filtered["Year-Of-Publication"], errors="coerce")
        filtered = books_filtered[books_filtered["Year-Of-Publication"] == year]

        # Sort judul secara alfabet
        filtered = filtered.sort_values("Book-Title")

        total = len(filtered)
        start = (page - 1) * size
        end = start + size
        return {
            "total": total,
            "page": page,
            "books": filtered.iloc[start:end].fillna("").to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))