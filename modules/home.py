# modules/home.py
import streamlit as st

def show():
    st.title("KBS Tanggap Darurat Kesehatan")
    st.markdown("""
    #### Sistem Knowledge-Based untuk Efisiensi Tanggap Darurat Kesehatan Masyarakat
    Selamat datang di aplikasi KBS!  
    Sistem ini membantu pengambilan keputusan dalam penanganan insiden darurat kesehatan menggunakan kecerdasan buatan (AI) dan rule base.
    ---
    **Fitur utama:**
    - Input & prediksi insiden secara realtime
    - Rekomendasi tindakan berbasis model & aturan
    - Dashboard visualisasi tren dan pola kasus
    - Notifikasi jika waktu respons terlalu lama

    Silakan pilih menu di sidebar untuk mulai 🚑
    """)
