import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load API Key Gemini dari .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  # atau 'gemini-1.5-flash' / 'gemini-2.0-flash'

# Load data
books = pd.read_csv("data/processed/books_cleaned.csv")
book_embeddings = np.load("models/saved/book_embeddings_fp16.npy").astype(np.float32)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# === Fungsi LLM ===
def generate_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return f"[Error] {e}"

# === Fungsi Utama RAG ===
def get_rag_response(query: str, top_k=5) -> str:
    query_vec = embed_model.encode([query])
    scores = cosine_similarity(query_vec, book_embeddings)[0]
    top_idx = scores.argsort()[::-1][:top_k]
    top_books = books.iloc[top_idx]

    context = "\n".join(
        f"- {row['Book-Title']} by {row['Book-Author']} ({row['Year-Of-Publication']})"
        for _, row in top_books.iterrows()
    )

    prompt = f""" Anda adalah seorang Customer service perpustakaan digital
    User menanyakan: "{query}"

    Dan ini adalah daftar buku yang relevan yang ada di perpustakaan:

    {context}

   Mohon rekomendasikan buku terbaik dan jelaskan alasannya kepada pengguna tersebtu.
    """.strip()

        # Panggil Gemini
    response = generate_gemini_response(prompt)

    # Tambahkan fallback jika ada error
    if response.startswith("[Error"):
        fallback = f"""❌ Assistant failed to respond using Gemini.\n\nHere are relevant books instead:\n\n{context}"""
        return fallback
    else:
        return response
