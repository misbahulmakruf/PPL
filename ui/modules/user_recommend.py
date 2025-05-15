import streamlit as st
import requests
import pandas as pd
from components.layout import show_book_grid

API_URL = "http://localhost:8000"

def show_user_recommend():
    st.header("User-Based Recommendations")
    
    # Load user data
    try:
        users_df = pd.read_csv("data/raw/Users.csv")
        user_options = users_df['User-ID'].tolist()
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
        return
    
    # User selection
    selected_user = st.selectbox(
        "Select a user ID",
        options=user_options,
        format_func=lambda x: f"User {x}"
    )
    
    if st.button("Get Recommendations"):
        try:
            # Get recommendations from API
            response = requests.get(f"{API_URL}/recommend/user/{selected_user}")
            if response.status_code == 200:
                data = response.json()
                recommendations = data["recommendations"]
                
                # Display recommendations
                st.subheader("Recommended Books")
                for book in recommendations:
                    with st.container():
                        st.markdown(f"""
                            <div class="book-card">
                                <div class="book-title">{book['title']}</div>
                                <div class="book-author">by {book['author']}</div>
                                <div class="book-year">Published: {book['year']}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error(f"Error getting recommendations: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Add some helpful information
    with st.expander("ℹ️ How to find your User ID"):
        st.markdown("""
            Your User ID is a unique number that identifies you in our system. You can find it:
            1. In your profile settings
            2. In your reading history
            3. By contacting our support team
        """)
