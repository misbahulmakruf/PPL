import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Load data ---
@st.cache_data(show_spinner=False)
def load_books():
    df = pd.read_csv("data/raw/Books.csv")
    df = df[["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication"]].dropna()
    return df.reset_index(drop=True)

# --- Embed books once ---
@st.cache_resource(show_spinner=True)
def embed_books(titles, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(titles.tolist(), show_progress_bar=True)
    return model, embeddings

# --- Retrieve similar books based on query ---
def retrieve_similar_books(query, book_titles, book_embeddings, model, top_k=5):
    query_vec = model.encode([query])
    scores = cosine_similarity(query_vec, book_embeddings)[0]
    top_idx = scores.argsort()[::-1][:top_k]
    return top_idx, scores[top_idx]

# --- Main assistant UI ---
def show_ai_assistant_rag():
    st.title("AI Book Assistant (RAG)")
    st.markdown("Ask a question like: `recommend fantasy books` or `what's similar to Atomic Habits`")

    books = load_books()
    model, book_embeddings = embed_books(books["Book-Title"])

    # Display chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("Type your book-related question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        idx, scores = retrieve_similar_books(prompt, books["Book-Title"], book_embeddings, model)
        top_books = books.iloc[idx]

        response = "Here are some books I think you'll like:\n\n"
        for i, row in top_books.iterrows():
            response += f"- **{row['Book-Title']}** by *{row['Book-Author']}* ({row['Year-Of-Publication']})\n"

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
