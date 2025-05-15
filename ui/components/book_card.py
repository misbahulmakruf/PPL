import streamlit as st
from components.utils import get_cover_url

def generate_book_card_html(book, with_rating=False):
    """
    Generate HTML string for a book card.
    """
    cover_url = (
        book.get('Image-URL-L') or
        (get_cover_url(book.get('isbn', '')) if book.get('isbn') else None) or
        "https://via.placeholder.com/120x180?text=No+Cover"
    )
    title = book.get('title', 'No Title')
    author = book.get('author', 'Unknown Author')
    year = book.get('year', '')
    publisher = book.get('publisher', '')
    description = book.get('description', '')

    book_info = f'<div class="book-title">{title}</div><div class="book-author">by {author}</div>'

    if with_rating:
        rating = book.get('predicted_rating') or book.get('score')
        if rating:
            stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
            book_info += f'<div class="book-rating">{stars} {rating:.1f}/5.0</div>'

    details = []
    if year:
        details.append(f"Published: {year}")
    if publisher:
        details.append(f"Publisher: {publisher}")
    if details:
        book_info += f'<div class="book-details">{" | ".join(details)}</div>'

    if description:
        book_info += f'<div class="book-description">{description}</div>'

    return f"""
    <div class="book-card">
        <div class="book-cover-container">
            <img src="{cover_url}" alt="{title} cover" class="book-cover">
        </div>
        <div class="book-info">
            {book_info}
        </div>
    </div>
    """
