import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tqdm import tqdm

# Load book data
books = pd.read_csv("data/raw/Books.csv", encoding="latin-1", on_bad_lines='skip')
books = books.dropna(subset=['ISBN', 'Book-Title', 'Book-Author'])
books['combined_features'] = books['Book-Title'].fillna('') + " " + books['Book-Author'].fillna('')

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english', max_features=20000)
tfidf_matrix = tfidf.fit_transform(books['combined_features'])

# Build mappings
isbn_to_index = pd.Series(books.index, index=books['ISBN']).drop_duplicates()
index_to_isbn = pd.Series(books['ISBN'].values, index=books.index)

# Precompute top-k cosine similarity
similarity_dict = {}

print("Precomputing similarities...")
for idx in tqdm(range(tfidf_matrix.shape[0])):
    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    top_indices = sim_scores.argsort()[::-1][1:6]  # Skip self, ambil 5 teratas

    similar = []
    for i in top_indices:
        similar.append({
            "isbn": index_to_isbn[i],
            "score": float(sim_scores[i])
        })

    similarity_dict[index_to_isbn[idx]] = similar

# Save artifacts
joblib.dump(similarity_dict, "models/saved/similarity_content_top5.pkl")
joblib.dump(books, "models/saved/books_cleaned.pkl")
print("Done.")
