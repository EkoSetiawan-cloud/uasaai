import streamlit as st
import pandas as pd
import joblib
import os

def show():
    st.header("Prediksi Hasil Penanganan & Waktu Respons")

    rf_path = "models/rf_model.pkl"
    reg_path = "models/regression_model.pkl"
    enc_path = "models/encoder.pkl"
    data_path = "data/simulasi_kasus_darurat.csv"

    if not os.path.isfile(rf_path) or not os.path.isfile(reg_path) or not os.path.isfile(enc_path):
        st.error("File model atau encoder belum ditemukan.")
        return

    rf_model = joblib.load(rf_path)
    reg_model = joblib.load(reg_path)
    encoder = joblib.load(enc_path)

    kategorik = ["Jenis Insiden", "Tingkat Keparahan", "Tindakan Awal", "Lokasi Kejadian"]
    num_cols = ["Jumlah Korban", "Waktu Respons Petugas (menit)"]

    # Load data dan ambil insiden terakhir yang belum diprediksi
    df = pd.read_csv(data_path)
    latest = df[df["Hasil Penanganan"].isna()].tail(1)  # atau .iloc[-1:] kalau ingin insiden terakhir

    if latest.empty:
        st.success("Tidak ada insiden baru yang perlu diprediksi.")
        return

    st.subheader("Data Insiden Terakhir (Belum ada prediksi):")
    st.dataframe(latest)

    # Preprocessing input data
    encoded = encoder.transform(latest[kategorik])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(kategorik))
    X_pred = pd.concat([encoded_df, latest[num_cols].reset_index(drop=True)], axis=1)

    # Prediksi hasil penanganan dan waktu respons
    hasil_prediksi = rf_model.predict(X_pred)[0]
    waktu_prediksi = reg_model.predict(X_pred)[0]

    st.success(f"Prediksi Hasil Penanganan: **{hasil_prediksi}**")
    st.info(f"Estimasi Waktu Respons: **{waktu_prediksi:.2f} menit**")

    # Optional: update hasil prediksi ke CSV
    if st.button("Update hasil prediksi ke data"):
        df.loc[latest.index, "Hasil Penanganan"] = hasil_prediksi
        df.to_csv(data_path, index=False)
        st.success("Hasil prediksi telah diupdate ke file CSV.")
