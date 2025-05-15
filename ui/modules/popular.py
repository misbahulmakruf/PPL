import streamlit as st
import requests
from components.layout import show_book_grid, show_loading_spinner

API_URL = "http://localhost:8000"


def show_popular_books():
    st.header("Popular Books")
    spinner_slot = show_loading_spinner()

    try:
        response = requests.get("http://localhost:8000/popular")
        if response.status_code == 200:
            books = response.json()["books"]
        else:
            spinner_slot.empty()
            st.error("Failed to fetch books.")
            return
    except Exception as e:
        spinner_slot.empty()
        st.error(f"Error: {e}")
        return

    spinner_slot.empty()
    st.subheader("Most Popular Books")
    show_book_grid(books)
