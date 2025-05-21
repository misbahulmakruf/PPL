import streamlit as st
import requests
from components.layout import show_book_grid_columns, show_loading_spinner
from modules.popular import show_popular_books
from modules.random import show_random_books

def show_dashboard_with_search():
    # --- Hero Section ---
    st.html("""<style>
        .hero-section {
            background: linear-gradient(to right, #4a00e0, #8e2de2);
            color: white;
            padding: 5rem 2rem;
            border-radius: 16px;
            text-align: center;
            margin-top: 2rem;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            font-family: 'Segoe UI', sans-serif;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
            letter-spacing: 1px;
        }
        .hero-subtitle {
            font-size: 1.25rem;
            font-weight: 300;
            opacity: 0.95;
        }
    </style>
    <div class="hero-section">
        <div class="hero-title">📚 Welcome to BookVerse</div>
        <div class="hero-subtitle">Sahabat Rekomendasi Bacaan Anda</div>
    </div>""")

    # --- Search Section ---
    st.markdown("### Pencarian Buku")
    col1, col2 = st.columns([6, 1])

    with col1:
        title_query = st.text_input("Masukkan judul atau kata kunci", key="dashboard_search")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("🔎 Cari", key="dashboard_button")

    if search_clicked and title_query.strip():
        try:
            with st.spinner("Searching..."):
                api_url = "http://127.0.0.1:8000/search_and_recommend"
                params = {"title_query": title_query}
                response = requests.get(api_url, params=params)
                data = response.json()

            if response.status_code != 200:
                st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")
            else:
                st.subheader("📘 Buku Ditemukan")
                st.success(f"Menemukan buku yang mirip dengan: {data['original']['title']}")

                original_book = data["original"]
                original_card = {
                    "isbn": original_book.get("isbn"),
                    "title": original_book.get("title"),
                    "author": original_book.get("author"),
                    "publisher": original_book.get("publisher"),
                    "year": original_book.get("year"),
                    "score": original_book.get("score") / 10,
                    "Image-URL-L": f"http://covers.openlibrary.org/b/isbn/{original_book.get('isbn')}-L.jpg"
                }

                show_book_grid_columns([original_card], with_rating=True)

                st.subheader("📚 Rekomendasi")
                show_book_grid_columns(data["recommendations"], with_rating=True)

        except Exception as e:
            st.error(f"❌ Failed to fetch recommendation: {e}")

    # --- Style tombol ---
    st.html("""<style>
        .stButton button {
            background-color: #2E3192;
            color: white;
            padding: 0.5rem 1.2rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
        }
        .stButton button:hover {
            background-color: #1b1e6b;
        }
    </style>""")

    # --- Tabs for Popular and Random ---
    st.markdown("### 📖 Jelajahi Buku")
    tab1, tab2 = st.tabs(["🔥 Buku Populer", "🎲 Temukan Buku secara Acak"])

    with tab1:
        show_popular_books()

    with tab2:
        show_random_books()
