# Buat struktur folder dasar untuk UI
mkdir -p book_recommendation_system/ui/assets
mkdir -p book_recommendation_system/ui/pages
mkdir -p book_recommendation_system/ui/components

# Buat file placeholder
touch book_recommendation_system/ui/app.py
touch book_recommendation_system/ui/pages/book_details.py
touch book_recommendation_system/ui/components/sidebar.py
touch book_recommendation_system/ui/components/book_card.py

# Unduh gambar placeholder untuk cover buku yang tidak tersedia
curl -o book_recommendation_system/ui/assets/no_cover.png https://via.placeholder.com/150x200.png?text=No+Cover
# Catatan: Anda mungkin perlu membuat file placeholder ini secara manual jika curl tidak tersedia

# Buat file .env untuk konfigurasi
echo "API_URL=http://localhost:8000" > book_recommendation_system/.env