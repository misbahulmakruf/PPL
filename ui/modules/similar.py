import streamlit as st
import requests
from components.layout import show_book_grid, show_loading_spinner

API_URL = "http://localhost:8000"

def show_similar_books():
    st.header("🔍 Find Similar Books by Title")

    title_input = st.text_input("Enter part of a book title")

    if st.button("Find Similar Books") and title_input.strip():
        spinner_slot = show_loading_spinner()

        try:
            # Cari ISBN dari title
            search_response = requests.get(f"{API_URL}/search", params={"title": title_input})
            if search_response.status_code != 200:
                spinner_slot.empty()
                st.error("Book not found.")
                return

            isbn = search_response.json()["ISBN"]
            found_title = search_response.json()["Book-Title"]

            # Lanjut ke pencarian similar books
            response = requests.get(f"{API_URL}/similar/{isbn}")
            if response.status_code == 200:
                similar_books = response.json()["similar_books"]
            else:
                spinner_slot.empty()
                st.error(f"Error getting similar books: {response.json().get('detail', 'Unknown error')}")
                return
        except Exception as e:
            spinner_slot.empty()
            st.error(f"Error: {str(e)}")
            return

        spinner_slot.empty()
        st.success(f"Showing similar books to: **{found_title}**")
        st.subheader("📚 Similar Books")
        show_book_grid(similar_books)
