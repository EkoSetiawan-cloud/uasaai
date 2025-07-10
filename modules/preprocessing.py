# modules/preprocessing.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

def show():
    st.header("Preprocessing Data Kasus Darurat")

    csv_path = "data/simulasi_kasus_darurat.csv"
    # Load data
    try:
        df = pd.read_csv(csv_path)
    except:
        st.error("File data simulasi_kasus_darurat.csv tidak ditemukan!")
        return

    st.subheader("Preview Data Asli")
    st.dataframe(df.head())

    # 1. Hapus duplikat
    df = df.drop_duplicates()
    
    # 2. Imputasi missing value tingkat keparahan (modus)
    if df['Tingkat Keparahan'].isnull().sum() > 0:
        modus_keparahan = df['Tingkat Keparahan'].mode()[0]
        df['Tingkat Keparahan'] = df['Tingkat Keparahan'].fillna(modus_keparahan)

    # 3. One-hot encoding atribut kategorik
    kategorik = ["Jenis Insiden", "Tingkat Keparahan", "Tindakan Awal", "Lokasi Kejadian"]
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(df[kategorik])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(kategorik))

    # 4. Normalisasi waktu respons
    scaler = MinMaxScaler()
    df["Waktu Respons Petugas (menit)_Norm"] = scaler.fit_transform(df[["Waktu Respons Petugas (menit)"]])

    # 5. Gabungkan hasil encoding & numerik
    df_final = pd.concat([df.reset_index(drop=True), encoded_df], axis=1)
    
    # 6. SMOTE balancing untuk kelas minoritas (jika perlu)
    # Misal untuk field "Hasil Penanganan", target = "Meninggal"
    # (Optional, diaktifkan hanya jika kelas imbalance)
    # from collections import Counter
    # st.write("Distribusi sebelum SMOTE:", dict(Counter(df_final["Hasil Penanganan"])))
    # smote = SMOTE(random_state=42)
    # X_res, y_res = smote.fit_resample(df_final.drop(["Hasil Penanganan"], axis=1), df_final["Hasil Penanganan"])
    # st.write("Distribusi sesudah SMOTE:", dict(Counter(y_res)))

    # 7. Tampilkan data hasil preprocessing
    st.subheader("Preview Data Setelah Preprocessing (One-hot & Normalisasi)")
    st.dataframe(df_final.head())

    # (Optional) Export data hasil preprocessing
    st.download_button("Download Data Preprocessing (CSV)", df_final.to_csv(index=False), "data_preprocessed.csv", "text/csv")

