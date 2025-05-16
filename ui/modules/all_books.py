import streamlit as st
import requests

API_URL = "http://localhost:8000"

def show_all_books_filtered(page_size=20):
    st.title("📚 Semua Buku")

    # Show spinner while fetching year range
    with st.spinner("Memuat data tahun..."):
        response = requests.get("http://127.0.0.1:8000/year_range")
    if response.status_code == 200:
        year_data = response.json()
        year_range = st.slider("Pilih rentang tahun terbit:",
                               min_value=year_data["min"],
                               max_value=year_data["max"],
                               value=(2000, 2020))
    else:
        st.error("Gagal mengambil data tahun.")
        return

    page = st.number_input("Halaman", min_value=1, step=1)

    if st.button("🔍 Tampilkan Buku"):
        with st.spinner("Sedang memuat..."):
            params = {
                "page": page,
                "size": page_size,
                "year_start": year_range[0],
                "year_end": year_range[1]
            }
            try:
                response = requests.get("http://127.0.0.1:8000/books_by_year_range", params=params)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"{len(data['books'])} buku ditampilkan dari tahun {year_range[0]}–{year_range[1]}")
                    st.dataframe(data["books"])
                else:
                    st.error(f"Error: {response.status_code} - {response.json()['detail']}")
            except Exception as e:
                st.error(f"Gagal memuat data: {e}")

