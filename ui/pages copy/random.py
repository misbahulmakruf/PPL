import streamlit as st
import requests
from components.layout import show_book_grid, show_loading_spinner

API_URL = "http://localhost:8000"

def show_random_books():
    st.header("🎲 Random Book Discovery")

    if st.button("Discover Random Books"):
        spinner_slot = show_loading_spinner()  # ✅ tampilkan spinner dan simpan reference

        try:
            response = requests.get(f"{API_URL}/random")
            if response.status_code == 200:
                books = response.json()["books"]
            else:
                spinner_slot.empty()  # ✅ hilangkan spinner saat error
                st.error(f"Error getting random books: {response.json()['detail']}")
                return
        except Exception as e:
            spinner_slot.empty()
            st.error(f"Error: {str(e)}")
            return

        spinner_slot.empty()  # ✅ hilangkan spinner setelah sukses

        st.subheader("🎉 Random Book Selection")
        show_book_grid(books)
