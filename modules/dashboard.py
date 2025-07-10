# modules/dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():
    st.header("📊 Dashboard Insight Kasus Darurat")

    data_path = "data/simulasi_kasus_darurat.csv"
    try:
        df = pd.read_csv(data_path)
    except:
        st.error("File data tidak ditemukan!")
        return

    st.subheader("Statistik Jumlah Insiden per Outcome")
    st.bar_chart(df["Hasil Penanganan"].value_counts())

    st.subheader("Tren Jumlah Insiden per Bulan")
    df['Tanggal'] = pd.to_datetime(df['Tanggal & Waktu Kejadian'].str.split().str[0], errors='coerce')
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    insiden_per_bulan = df.groupby('Bulan').size()
    st.line_chart(insiden_per_bulan)

    st.subheader("Rata-rata Waktu Respons per Outcome")
    avg_respons = df.groupby("Hasil Penanganan")["Waktu Respons Petugas (menit)"].mean()
    st.bar_chart(avg_respons)

    st.subheader("Distribusi Jenis Insiden")
    st.bar_chart(df["Jenis Insiden"].value_counts())

    st.subheader("Distribusi Lokasi Kejadian (Top 6)")
    lokasi = df["Lokasi Kejadian"].value_counts().head(6)
    fig, ax = plt.subplots()
    ax.pie(lokasi, labels=lokasi.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # ==============================
    # Insight dan Rekomendasi Otomatis
    # ==============================
    st.subheader("📌 Insight & Rekomendasi Otomatis")

    # 1. Wilayah dengan kasus "Meninggal" terbanyak
    df_meninggal = df[df["Hasil Penanganan"] == "Meninggal"]
    if not df_meninggal.empty:
        top_wilayah_meninggal = df_meninggal["Lokasi Kejadian"].value_counts().idxmax()
        total_meninggal = df_meninggal["Lokasi Kejadian"].value_counts().max()
        st.warning(f"⚠️ Wilayah dengan insiden meninggal terbanyak: **{top_wilayah_meninggal}** ({total_meninggal} kasus)")
    else:
        st.info("Tidak ada kasus meninggal dalam data ini.")

    # 2. Jenis insiden dengan outcome "Dirujuk" terbanyak
    df_dirujuk = df[df["Hasil Penanganan"] == "Dirujuk"]
    if not df_dirujuk.empty:
        top_jenis_dirujuk = df_dirujuk["Jenis Insiden"].value_counts().idxmax()
        total_dirujuk = df_dirujuk["Jenis Insiden"].value_counts().max()
        st.warning(f"🚑 Jenis insiden paling sering dirujuk: **{top_jenis_dirujuk}** ({total_dirujuk} kasus)")
    else:
        st.info("Tidak ada kasus dirujuk dalam data ini.")

    # 3. Bulan dengan insiden terbanyak
    if not df['Bulan'].empty:
        top_bulan = df['Bulan'].value_counts().idxmax()
        jumlah_bulan = df['Bulan'].value_counts().max()
        st.info(f"📅 Bulan dengan kasus terbanyak: **{top_bulan}** ({jumlah_bulan} kasus)")

    # 4. Outcome dengan rata-rata waktu respons terlama
    if not avg_respons.empty:
        outcome_lama = avg_respons.idxmax()
        waktu_lama = avg_respons.max()
        st.info(f"⏱️ Rata-rata waktu respons terlama: **{outcome_lama}** ({waktu_lama:.1f} menit)")

    # 5. Rekomendasi otomatis
    if not df_meninggal.empty and waktu_lama > 30:
        st.error("🚨 Rekomendasi: Perkuat respon cepat di wilayah/kategori di atas, karena waktu respons rata-rata cukup lama (>30 menit) dan outcome fatal meningkat!")
    elif not df_meninggal.empty:
        st.success("✅ Rekomendasi: Lakukan analisis lebih lanjut pada wilayah/kategori meninggal, walau waktu respons tidak terlalu lama.")
    else:
        st.success("👍 Tidak ada indikasi masalah kritis pada data ini. Tetap pertahankan kualitas respon.")

    st.caption("Insight ini dihasilkan otomatis berdasarkan analisis tren data terbaru.")
