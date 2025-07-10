# modules/input.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import os

def show():
    st.header("Input Data Insiden Darurat")
    csv_path = "data/simulasi_kasus_darurat.csv"
    columns = [
        "ID Kasus",
        "Tanggal & Waktu Kejadian",
        "Lokasi Kejadian",
        "Jenis Insiden",
        "Tingkat Keparahan",
        "Jumlah Korban",
        "Waktu Respons Petugas (menit)",
        "Tindakan Awal",
        "Hasil Penanganan"
    ]

    with st.form("input_insiden"):
        tanggal = st.date_input("Tanggal Kejadian", value=datetime.today())
        waktu = st.time_input("Waktu Kejadian", value=datetime.now().time())
        kecamatan = st.selectbox("Kecamatan", 
            ["Batam Kota", "Lubuk Baja", "Bengkong", "Sekupang", "Nongsa", "Sagulung"])
        kelurahan = st.selectbox("Kelurahan", 
            ["Baloi Indah", "Tiban Baru", "Sadai", "Tanjung Buntung", "Duriangkang", "Batu Besar"])
        jenis_insiden = st.selectbox("Jenis Insiden", 
            ["Kecelakaan Lalu Lintas", "Kebakaran", "Keracunan", "Bencana Alam", "Kejadian Lain"])
        keparahan = st.selectbox("Tingkat Keparahan", ["Ringan", "Sedang", "Berat"])
        korban = st.number_input("Jumlah Korban", min_value=1, max_value=20, value=1)
        waktu_respons = st.number_input("Waktu Respons Petugas (menit)", min_value=1, max_value=180, value=10)
        tindakan = st.selectbox("Tindakan Awal", [
            "CPR",
            "Imobilisasi",
            "Observasi",
            "Pemberian Obat",
            "Pemberian Oksigen"
        ])
        submitted = st.form_submit_button("Simpan Data")

    if submitted:
        # Generate ID Kasus otomatis dan urut
        if os.path.isfile(csv_path):
            df_lama = pd.read_csv(csv_path)
            if "ID Kasus" in df_lama.columns and len(df_lama) > 0:
                last_id = df_lama["ID Kasus"].iloc[-1]
                try:
                    next_num = int(str(last_id).split("-")[-1]) + 1
                except:
                    next_num = len(df_lama) + 1
            else:
                next_num = 1
        else:
            next_num = 1

        id_kasus_baru = f"KSD-{next_num:04d}"

        # Safety: Pastikan tipe benar
        if not isinstance(tanggal, date):
            tanggal = datetime.today().date()
        if not isinstance(waktu, time):
            waktu = datetime.now().time()

        # Format tanggal & waktu: m/d/yyyy H:MM:SS
        tanggal_waktu = f"{tanggal.month}/{tanggal.day}/{tanggal.year} {waktu.hour}:{waktu.minute:02d}:{waktu.second:02d}"

        data_baru = {
            "ID Kasus": id_kasus_baru,
            "Tanggal & Waktu Kejadian": tanggal_waktu,
            "Lokasi Kejadian": f"{kecamatan}/{kelurahan}",
            "Jenis Insiden": jenis_insiden,
            "Tingkat Keparahan": keparahan,
            "Jumlah Korban": korban,
            "Waktu Respons Petugas (menit)": waktu_respons,
            "Tindakan Awal": tindakan,
            "Hasil Penanganan": ""
        }

        df_baru = pd.DataFrame([data_baru], columns=columns)
        file_exists = os.path.isfile(csv_path)

        if file_exists:
            df_baru.to_csv(csv_path, mode='a', index=False, header=False)
        else:
            df_baru.to_csv(csv_path, mode='w', index=False, header=True)

        st.success("Data insiden berhasil disimpan ke CSV!")
        st.json(data_baru)
