import streamlit as st
import requests
import pandas as pd
from modules.user_recommend import show_user_recommend
from modules.popular import show_popular_books
from modules.random import show_random_books
from modules.similar import show_similar_books
from modules.home import show_dashboard_with_search
import streamlit.components.v1 as components
import os
# API configuration
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Book Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
# def load_css(path="static/style.css"):
#     with open(path) as f:
#         st.html(f"<style>{f.read()}</style>")

# Panggil di awal app.py



def load_css(path="static/style.css"):
    css_path = os.path.join(os.path.dirname(__file__), path)
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ CSS file not found at: {css_path}")

load_css("static/style.css")
# Sidebar with modern design
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/book-shelf.png", width=80)
    st.title("Book Recommender")
    st.markdown("---")
    
    # Navigation menu
    st.markdown("### 🎯 Navigation")
    page = st.radio(
        "Choose a section",
        ["📚 Popular Books", "🎲 Random Discovery", "🔍 Similar Books", "💬 AI Assistant"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
        ### 📖 About
        Discover your next favorite book with our intelligent recommendation system.
        
        ### ✨ Features
        - Smart book recommendations
        - Popular book trends
        - Random book discovery
        - AI-powered book suggestions
    """)

# Main content area
st.title("📚 Book Recommendation System")

# AI Chatbot Component
def show_chatbot():
    st.markdown("### 💬 AI Book Assistant")
    st.markdown("Ask me anything about books or get personalized recommendations!")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about books..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Simulate AI response (replace with actual AI integration)
        with st.chat_message("assistant"):
            response = "I'm your AI book assistant! I can help you find great books to read. What kind of books do you enjoy?"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Main content routing
if page == "📚 Popular Books":
    show_popular_books()
elif page == "🎲 Random Discovery":
    show_random_books()
elif page == "🔍 Similar Books":
    show_similar_books()
elif page == "💬 AI Assistant":
    show_chatbot()
elif page == "Home":
    show_dashboard_with_search()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Made with ❤️ by Book Recommender Team
    </div>
    """,
    unsafe_allow_html=True
)