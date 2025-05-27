# 📚 Sistem Rekomendasi Buku 🚀

---

## 🔹 Konsep Utama

* Sistem rekomendasi buku modern
* Dibangun dengan **FastAPI** (backend API) dan **Streamlit** (frontend UI)

---

## ✨ Fitur Utama

* ✅ Rekomendasi buku yang dipersonalisasi
* 🔥 Buku populer dan sedang tren
* 🎲 Penemuan buku acak
* 🧠 Rekomendasi berbasis konten dan *collaborative filtering*
* 🔍 Pencarian buku berdasarkan judul
* 🤖 **Asisten interaktif** (baru!)
* 🖥️ UI modern dan interaktif

---

## 📂 Struktur Proyek

```
book_recommender_system/
├── api/        # FastAPI backend
├── ui/         # Streamlit frontend
├── data/       # Data mentah dan yang sudah diproses
├── models/     # Model yang disimpan
└── README.md
```

---

## 🚀 Cara Memulai

### 1. Klon Repositori

```bash
git clone https://github.com/misbahulmakruf/PPL
cd book_recommender_system
```

### 2. Instal Dependensi

```bash
pip install -r requirement.txt
```

### 3. Siapkan Data

* Download dataset melalui Google Drive: [Google Drive](https://drive.google.com/drive/u/1/folders/1f2Gn93Hj8RqfveRDna19Y8eL-N72Q9Yo)
* Letakkan berkas:

  * `Books.csv`, `Ratings.csv`, `Users.csv` ke dalam `data/raw/`
  * `book_clean.csv` ke dalam `data/processed/`
  * `similiarity_cbf.pkl`, `books_cleaned.pkl`, `book_embeddings.npy` ke dalam `models/saved/`

### 4. Membuat File `.env` dari `.env_temp`

Anda sudah memiliki file `.env_temp` di repositori Anda. Ganti nama menjadi `.env`:

* Buka direktori proyek
* Cari file `.env_temp`
* Ganti nama menjadi `.env`

Isi file `.env`:

```
GOOGLE_API_KEY=your_google_api_key
```

Ganti `your_google_api_key` dengan API key Google Gemini Anda.

---

## 🔹 Cara Mendapatkan Google Gemini API Key

1. **Buka Google Cloud Console:** [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. **Pilih atau Buat Proyek:**

   * Klik "New Project" jika belum ada proyek
3. **Aktifkan Gemini API:**

   * Cari "Generative Language API"
   * Klik dan tekan "Enable"
4. **Buat Kredensial API Key:**

   * Navigasi ke *APIs & Services* > *Credentials*
   * Klik "+ CREATE CREDENTIALS" > *API Key*
   * Salin API key tersebut
5. **Update `.env`:**

```env
GOOGLE_API_KEY=AIzaSy...YOUR_ACTUAL_API_KEY...
```

---

### 5. Jalankan Backend (FastAPI)

```bash
uvicorn api.main:app --reload
```

Akses di: [http://localhost:8000](http://localhost:8000)

### 6. Jalankan Frontend (Streamlit)

```bash
streamlit run ui/app.py
```

Akses di: [http://localhost:8501](http://localhost:8501)

---

## 🔗 *Endpoint* API

* `/` : Selamat datang 👋
* `/health` : Cek kesehatan ❤️‍🩹
* `/recommend/user/{user_id}` : Rekomendasi untuk pengguna 👤
* `/popular` : Buku populer 🔥
* `/random` : Buku acak 🎲
* `/similar_content/{isbn}` : Buku serupa (berbasis konten) 📚
* `/search?title=...` : Cari buku 🔎
* `/newest` : Buku terbaru ✨
* `/assistant` : Asisten buku 🤖

---

## 🧑‍💻 Kontributor

* Dikembangkan oleh Tim Rekomendasi Buku (KELOMPOK 5)
* Misbahul Makruf
* Najwan Yusnianda
* Fadhallah
* Nuwairy El Furqany
* Irwan Saputra
* Mukhlisin

---

## 🙏 Kontribusi

* Jangan ragu untuk berkontribusi atau membuka *issue*!
