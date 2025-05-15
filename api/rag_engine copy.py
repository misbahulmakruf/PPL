import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy as np
from sentence_transformers import SentenceTransformer

# Load precomputed
books = pd.read_csv("data/processed/books_clean.csv")
book_embeddings = np.load("model/saved/book_embeddings.npy")
print("Loaded embeddings shape:", book_embeddings.shape)
print("First title:", books.iloc[0]["Book-Title"])
# Re-load model (tidak re-encode)
model = SentenceTransformer('all-MiniLM-L6-v2')
#book_embeddings = model.encode(books["Book-Title"].tolist(), show_progress_bar=True)

# RAG processing
def get_rag_response(query: str, top_k=5) -> str:
    query_vec = model.encode([query])
    scores = cosine_similarity(query_vec, book_embeddings)[0]
    top_idx = scores.argsort()[::-1][:top_k]
    top_books = books.iloc[top_idx]

    context = "\n".join(
        f"- {row['Book-Title']} by {row['Book-Author']} ({row['Year-Of-Publication']})"
        for _, row in top_books.iterrows()
    )

    full_prompt = f"""
You are a helpful book assistant. Based on the following user's query and a list of books, recommend one or more books and explain why.

Query: {query}

Relevant books:
{context}

Answer:
""".strip()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": full_prompt, "stream": False}
        )
        return response.json().get("response", "[No response from model]")
    except Exception as e:
        return f"Error: {e}"
