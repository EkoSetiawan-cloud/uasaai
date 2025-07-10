import streamlit as st
from modules import home, input, preprocessing, prediksi, dashboard, evaluasi

st.set_page_config(page_title="KBS Tanggap Darurat Kesehatan", layout="wide")

menu = st.sidebar.radio(
    "Navigasi Menu",
    [
        "🏠 Home",
        "📥 Input Data Insiden",
        "⚙️ Preprocessing",
        "🤖 Prediksi & Rekomendasi",
        "📊 Dashboard",
        "🧪 Evaluasi Model",
    ]
)

if menu == "🏠 Home":
    home.show()
elif menu == "📥 Input Data Insiden":
    input.show()
elif menu == "⚙️ Preprocessing":
    preprocessing.show()
elif menu == "🤖 Prediksi & Rekomendasi":
    prediksi.show()
elif menu == "📊 Dashboard":
    dashboard.show()
elif menu == "🧪 Evaluasi Model":
    evaluasi.show()
