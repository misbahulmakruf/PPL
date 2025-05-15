import streamlit as st
import requests
from components.layout import show_book_grid_columns, show_loading_spinner

API_URL = "http://localhost:8000"

def show_popular_books():
    spinner_slot = show_loading_spinner()

    try:
        response = requests.get(f"{API_URL}/popular")
        if response.status_code == 200:
            books = response.json()["books"]
        else:
            spinner_slot.empty()
            st.error("❌ Gagal mengambil data buku populer dari server.")
            return
    except Exception as e:
        spinner_slot.empty()
        st.error(f"⚠️ Error: {e}")
        return

    spinner_slot.empty()
    st.subheader("📈 Buku-Buku yang Sedang Populer")
    show_book_grid_columns(books, with_rating=True)
