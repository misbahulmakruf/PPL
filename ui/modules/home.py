import streamlit as st
import requests
from components.layout import show_book_grid, show_loading_spinner
def show_dashboard_with_search():
    st.html("""
        <div class="header">
            <h1 class="site-title">📚 BookVerse Dashboard</h1>
            <p class="site-subtitle">Search & discover what's new</p>
        </div>
    """)

    # --- Search section ---
    st.markdown("### 🔍 Search Similar Books")
    title_query = st.text_input("Enter book title or keyword", key="dashboard_search")
    if st.button("🔎 Search", key="dashboard_button") and title_query.strip():
        from modules.similar import show_similar_books
        show_similar_books(title_query)
        st.markdown("---")

    # --- Newest Books section ---
    try:
        res = requests.get("http://localhost:8000/popular")
        res.raise_for_status()
        new_books = res.json().get("books", [])
    except Exception as e:
        st.error(f"Failed to load newest books: {e}")
        return

    if new_books:
        st.markdown("### 🆕 Newest Books")
        show_book_grid(new_books[:10])
    else:
        st.warning("No new books found.")