import pandas as pd
import numpy as np

def get_top_n_recommendations(user_id, ratings, books, model=None, top_n=5):
    """
    Recommend top N books for a user using a trained model (e.g. Surprise SVD)
    """
    if model is None:
        try:
            from api.load_model import model  # lazy load model
        except ImportError:
            raise ValueError("Model is not available or load_model.py not found")

    if ratings is None or books is None:
        return []

    all_books = ratings['isbn'].unique()
    rated_books = ratings[ratings['user_id'] == user_id]['isbn']
    books_to_predict = [isbn for isbn in all_books if isbn not in rated_books.values]

    predictions = []
    for isbn in books_to_predict:
        try:
            pred = model.predict(user_id, isbn).est
            predictions.append((isbn, pred))
        except:
            continue  # skip prediction errors

    top_n_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]

    result = []
    for isbn, score in top_n_predictions:
        title = books[books['ISBN'] == isbn]['Book-Title'].values
        title = title[0] if len(title) > 0 else 'Unknown'
        result.append({
            "isbn": isbn,
            "title": title,
            "predicted_rating": round(score, 2)
        })

    return result


def get_popular_books(ratings, books, n=6):
    """
    Get the most popular books based on average rating and number of ratings
    """
    if ratings is None or books is None:
        return []

    # Compute mean and count per ISBN
    book_stats = ratings.groupby('isbn')['rating'].agg(['mean', 'count']).reset_index()
    
    # Filter with minimum number of ratings
    min_ratings = 10
    book_stats = book_stats[book_stats['count'] >= min_ratings]
    
    # Sort by average rating descending
    book_stats = book_stats.sort_values('mean', ascending=False)

    top_books = []
    for _, row in book_stats.head(n).iterrows():
        isbn = str(row['isbn'])
        match = books[books['ISBN'] == isbn]
        if match.empty:
            continue
        book_info = match.iloc[0]
        year_raw = book_info['Year-Of-Publication']
        year = int(year_raw) if pd.notna(year_raw) and int(year_raw) > 1000 and int(year_raw) <= 2050 else None
        top_books.append({
            "isbn": isbn,
            "title": str(book_info['Book-Title']),
            "author": str(book_info['Book-Author']),
            "year": year,
            "publisher" : str(book_info['Publisher']),
            "score": round(float(row['mean']), 2)/10  # ⬅️ Tambahkan rating rata-rata
        })
    print(match.iloc[0])
    return top_books


def get_random_books(books, ratings, n=6):
    """
    Get n random books and attach average rating as score
    """
    if books is None or ratings is None:
        return []

    # 1. Hitung skor rata-rata dari ratings
    rating_stats = ratings.groupby('isbn')['rating'].mean().reset_index()
    rating_stats.rename(columns={'rating': 'score'}, inplace=True)

    # 2. Ambil n random books
    sample = books.sample(n=n).copy()

    # 3. Gabungkan skor ke sample berdasarkan ISBN
    sample = sample.merge(rating_stats, how='left', left_on='ISBN', right_on='isbn')

    # 4. Return data dalam format konsisten
    results = []
    for _, row in sample.iterrows():
        try:
            year_raw = row['Year-Of-Publication']
            year = int(year_raw) if pd.notna(year_raw) and int(year_raw) > 1000 and int(year_raw) <= 2050 else None
        except:
            year = None

        results.append({
            "isbn": row['ISBN'],
            "title": row['Book-Title'],
            "author": row['Book-Author'],
            "publisher": row['Publisher'],
            "year": year,
            "score": round(row['score'], 2)/10 if pd.notna(row['score']) else None
        })

    return results



def get_similar_books_cf(isbn, books, model=None, top_n=6):
    """
    Dummy collaborative similarity based on index (can be replaced with actual embedding-based similarity)
    For now, just return random books for demo
    """
    if books is None:
        return []

    # fallback: return random books as fake "similar"
    return get_random_books(books, n=top_n)
