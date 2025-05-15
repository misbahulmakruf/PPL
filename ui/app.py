import streamlit as st
import os
from modules.popular import show_popular_books
from modules.random import show_random_books
from modules.similar import show_similar_books
from modules.user_recommend import show_user_recommend
from modules.home import show_dashboard_with_search
from modules.assistant import show_ai_assistant_rag
# --- Page config ---
st.set_page_config(
    page_title="BookVerse",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load external CSS ---
def load_css(path="static/style.css"):
    css_path = os.path.join(os.path.dirname(__file__), path)
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ CSS file not found: {css_path}")

load_css()

static_path= os.path.join(os.path.dirname(__file__))
icon_path = os.path.join(os.path.dirname(__file__), "static", "icons", "book.png")

# --- Sidebar Navigation ---
with st.sidebar:
    st.image(icon_path, width=60)# ⬅️ logo Anda
    st.title("BookVerse")
    st.markdown("Discover your next favorite book")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        ["Home", "Popular Books", "Random Discovery", "AI Assistant"],
        index=0,
        key="nav"
    )

    st.markdown("---")
    st.caption("© 2025 BookVerse Team")

# --- Routing ---
if menu == "Home":
    show_dashboard_with_search()

elif menu == "Popular Books":
    st.title("Popular Books")
    show_popular_books()

elif menu == "Random Discovery":
    st.title("Discover Random Books")
    show_random_books()

elif menu == "Similar Books":
    st.title("Find Similar Books")
    title = st.text_input("Enter book title to search:")
    if st.button("Search") and title.strip():
        show_similar_books(title)

elif menu == "AI Assistant":
    show_ai_assistant_rag()

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #999;'>Made with ❤️ by BookVerse Team</div>",
    unsafe_allow_html=True
)
