import joblib

# Load data once
books = joblib.load("models/saved/books_cleaned_cbf.pkl")
similarity = joblib.load("models/saved/similarity_cbf.pkl")

# Fungsi API
def search_books_by_title(query, top_n=9):
    query = query.lower()
    matches = books[books['Book-Title'].str.lower().str.contains(query, na=False)]
    return matches.head(top_n)

def recommend_similar_books(isbn):
    if isbn not in similarity:
        return []
    
    result = []
    for item in similarity[isbn]:
        match = books[books['ISBN'] == item['isbn']]
        if match.empty: continue
        book_info = match.iloc[0]
        result.append({
            "isbn": item['isbn'],
            "title": book_info['Book-Title'],
            "author": book_info['Book-Author'],
            "year": int(book_info['Year-Of-Publication']) if str(book_info['Year-Of-Publication']).isdigit() else None,
            "publisher": book_info['Publisher'],
            "score": round(item['score'], 3)
        })
    return result
