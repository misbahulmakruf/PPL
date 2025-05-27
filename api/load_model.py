import pandas as pd
import pickle


model = SVD()
# training...
with open("svd_model.pkl", "wb") as f:
    pickle.dump(model, f)


# Load ratings dan books
ratings = pd.read_csv("data/processed/ratings_cleaned.csv", encoding="latin-1", on_bad_lines='skip')
books = pd.read_csv("data/processed/books_cleaned.csv", encoding="latin-1", on_bad_lines='skip')

# Bersihkan kolom
ratings.columns = ratings.columns.str.strip()
books.columns = books.columns.str.strip()

ratings = ratings[['User-ID', 'ISBN', 'Book-Rating']]
ratings.columns = ['user_id', 'isbn', 'rating']
ratings = ratings[ratings['rating'] > 0]  # hanya rating eksplisit

books["ISBN"] = books["ISBN"].astype(str)
ratings["user_id"] = ratings["user_id"].astype(int).astype(str)
ratings["isbn"] = ratings["isbn"].astype(str)

# Load model SVD dari pickle
with open("models/svd_model.pkl", "rb") as f:
    model = pickle.load(f)


# Clean ratings data
ratings.columns = ratings.columns.str.strip()
ratings = ratings[['User-ID', 'ISBN', 'Book-Rating']]
ratings.columns = ['user_id', 'isbn', 'rating']
ratings = ratings[ratings['rating'] > 0]

# Clean books data
books.columns = books.columns.str.strip()