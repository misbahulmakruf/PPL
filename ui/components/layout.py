import streamlit as st
from components.utils import get_cover_url
from components.book_card import generate_book_card_html


def inject_book_card_css():
    st.html("""
        <style>
        div.stApp div.book-card {
            display: flex;
            padding: 1.25rem;
            border-radius: 10px;
            margin: 1.25rem 0;
            background-color: white;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            width: 100%;
            max-width: 800px;
        }
        div.stApp div.book-card:hover {
            transform: translateY(-4px);
            box-shadow: rgba(0, 0, 0, 0.18) 0px 8px 24px;
        }
        div.stApp div.book-cover-container {
            flex: 0 0 120px;
            margin-right: 1.5rem;
            align-self: center;
        }
        div.stApp div.book-cover-container img {
            width: 120px;
            height: auto;
            max-height: 180px;
            object-fit: cover;
            border-radius: 6px;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 8px;
        }
        div.stApp div.book-info {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 0.5rem;
        }
        div.stApp div.book-title {
            font-size: 1.35rem;
            font-weight: 600;
            color: #2E3192;
            line-height: 1.4;
            margin-bottom: 0.25rem;
        }
        div.stApp div.book-author {
            color: #555;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
        }
        div.stApp div.book-rating {
            color: #FF8C00;
            font-size: 1rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        div.stApp div.book-details {
            margin: 0.5rem 0;
            font-size: 0.9rem;
            color: #666;
        }
        div.stApp div.book-description {
            font-size: 0.95rem;
            color: #444;
            line-height: 1.6;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
        }
        @media (max-width: 768px) {
            div.stApp div.book-card {
                flex-direction: column;
                align-items: center;
                text-align: center;
                padding: 1rem;
            }
            div.stApp div.book-cover-container {
                margin-right: 0;
                margin-bottom: 1rem;
            }
            div.stApp div.book-info {
                align-items: center;
            }
        }
        div.stApp div.book-list-container {
            background-color: #f9f9fa;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 8px;
        }
        </style>
    """)

def show_book_grid(books: list, *, with_rating: bool = False):
    if not books:
        st.warning("No books found. Try adjusting your search criteria.")
        return

    inject_book_card_css()

    # ----- gabung semua kartu jadi satu string -----
    cards_html = "".join(
        generate_book_card_html(book, with_rating=with_rating)
        for book in books
    )

    full_html = f"""
    <div class="book-list-container">
        {cards_html}
    </div>
    """

    st.html(full_html)  

    #st.html(html)

def show_loading_spinner():
    SPINNER_HTML = """
    <style>
    div.stApp div.loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
        margin: 1rem 0;
    }
    div.stApp div.spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(46, 49, 146, 0.2);
        border-top: 5px solid #2E3192;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    <div class="loading-spinner">
        <div class="spinner"></div>
    </div>
    """
    placeholder = st.empty()
    placeholder.html(SPINNER_HTML)
    return placeholder
