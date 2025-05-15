import streamlit as st
import math
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
def show_book_grid_columns(books: list, *, with_rating: bool = False):
    if not books:
        st.warning("No books found. Try adjusting your search criteria.")
        return

    st.markdown("""
    <style>
    .book-grid-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        justify-content: space-between;
        padding: 1rem 0;
    }

    .book-card-grid {
        background: white;
        flex: 0 0 calc(33% - 1rem);
        box-shadow: rgba(0, 0, 0, 0.06) 0px 4px 12px;
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: transform 0.2s ease;
    }

    .book-card-grid:hover {
        transform: translateY(-4px);
        box-shadow: rgba(0, 0, 0, 0.15) 0px 8px 20px;
    }

    .book-cover-grid {
        width: 120px;
        height: 180px;
        object-fit: cover;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        box-shadow: rgba(0, 0, 0, 0.08) 0px 2px 6px;
    }

    .book-title-grid {
        font-size: 1rem;
        font-weight: bold;
        color: #2E3192;
        margin: 0.25rem 0;
        line-height: 1.3;
    }

    .book-meta-grid {
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 0.5rem;
    }

    .book-rating-grid {
        font-size: 0.85rem;
        color: #FFA000;
        margin-top: 0.25rem;
    }

    @media (max-width: 900px) {
        .book-card-grid {
            flex: 0 0 calc(50% - 1rem);
        }
    }

    @media (max-width: 600px) {
        .book-card-grid {
            flex: 0 0 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    cards_html = ""
    for book in books:
        cover_url = (
            book.get('Image-URL-L')
            or f"http://covers.openlibrary.org/b/isbn/{book.get('isbn', '')}-L.jpg"
            or "https://via.placeholder.com/120x180?text=No+Cover"
        )
        title = book.get('title', 'No Title')
        publisher = book.get('publisher', 'Unknown Publisher')
        year = book.get('year', '')
        rating = book.get('predicted_rating') or book.get('score')

        card = f"""
        <div class="book-card-grid">
            <img src="{cover_url}" alt="{title} cover" class="book-cover-grid"/>
            <div class="book-title-grid">{title}</div>
            <div class="book-meta-grid">{publisher} ({year})</div>"""

        if with_rating and rating:
            rounded_rating = math.floor(rating * 10)
            stars = ("⭐" * rounded_rating) + "☆" * (10 - rounded_rating)
            card += f"""<div class="book-rating-grid">{stars} {rating*10:.1f}/10.0</div>"""

        card += "</div>"
        cards_html += card

    full_html = f"""
    <div class="book-grid-container">
        {cards_html}
    </div>
    """

    st.html(full_html)

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
