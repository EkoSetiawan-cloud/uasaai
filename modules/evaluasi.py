# modules/evaluasi.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def show():
    st.header("📊 Evaluasi Model Prediksi KBS")

    # Load data dan model
    data_path = "data/simulasi_kasus_darurat.csv"
    rf_path = "models/rf_model.pkl"
    reg_path = "models/regression_model.pkl"
    enc_path = "models/encoder.pkl"

    try:
        df = pd.read_csv(data_path)
        rf_model = joblib.load(rf_path)
        reg_model = joblib.load(reg_path)
        encoder = joblib.load(enc_path)
    except Exception as e:
        st.error(f"Data atau model tidak ditemukan: {e}")
        return

    # === Siapkan data dan fitur seperti saat training ===
    kategorik = ["Jenis Insiden", "Tingkat Keparahan", "Tindakan Awal", "Lokasi Kejadian"]
    num_cols = ["Jumlah Korban", "Waktu Respons Petugas (menit)"]

    df_eval = df.dropna(subset=["Hasil Penanganan"])
    encoded = encoder.transform(df_eval[kategorik])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(kategorik))
    X_eval = pd.concat([encoded_df, df_eval[num_cols].reset_index(drop=True)], axis=1)
    y_eval_cls = df_eval["Hasil Penanganan"].reset_index(drop=True)
    y_eval_reg = df_eval["Waktu Respons Petugas (menit)"].reset_index(drop=True)

    # --- Prediksi dengan model ---
    y_pred_cls = rf_model.predict(X_eval)
    y_pred_reg = reg_model.predict(X_eval)

    # === EVALUASI KLASIFIKASI ===
    st.subheader("Evaluasi Model Klasifikasi (Hasil Penanganan)")
    akurasi = accuracy_score(y_eval_cls, y_pred_cls)
    st.metric("Akurasi", f"{akurasi:.2%}")
    st.text("Classification Report:")
    st.text(classification_report(y_eval_cls, y_pred_cls))

    # Confusion Matrix
    st.text("Confusion Matrix:")
    cm = confusion_matrix(y_eval_cls, y_pred_cls)
    fig, ax = plt.subplots()
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=rf_model.classes_)
    disp.plot(ax=ax, cmap=plt.cm.Blues)
    st.pyplot(fig)

    # === EVALUASI REGRESI ===
    st.subheader("Evaluasi Model Regresi (Waktu Respons Petugas)")
    r2 = r2_score(y_eval_reg, y_pred_reg)
    mae = mean_absolute_error(y_eval_reg, y_pred_reg)
    rmse = np.sqrt(mean_squared_error(y_eval_reg, y_pred_reg))
    st.metric("R2 Score", f"{r2:.2f}")
    st.metric("MAE", f"{mae:.2f}")
    st.metric("RMSE", f"{rmse:.2f}")

    # Plot: Actual vs Predicted
    st.text("Plot: Aktual vs Prediksi Waktu Respons")
    fig2, ax2 = plt.subplots()
    ax2.scatter(y_eval_reg, y_pred_reg, alpha=0.7)
    ax2.plot([y_eval_reg.min(), y_eval_reg.max()], [y_eval_reg.min(), y_eval_reg.max()], 'r--', lw=2)
    ax2.set_xlabel("Aktual")
    ax2.set_ylabel("Prediksi")
    st.pyplot(fig2)

    # === INSIGHT EVALUASI OTOMATIS ===
    st.subheader("Insight Evaluasi Model Otomatis")
    if akurasi > 0.85:
        st.success(f"✅ Model klasifikasi sangat baik (akurasi > 85%).")
    elif akurasi > 0.7:
        st.info("⚠️ Model klasifikasi cukup baik, tapi masih bisa ditingkatkan (akurasi > 70%).")
    else:
        st.error("❌ Model klasifikasi kurang akurat. Cek data training & parameter model.")

    if rmse < 15 and r2 > 0.7:
        st.success("✅ Model regresi waktu respons sangat baik.")
    elif rmse < 20 and r2 > 0.5:
        st.info("⚠️ Model regresi cukup baik, masih ada error moderat.")
    else:
        st.error("❌ Model regresi kurang akurat. Cek data training & fitur input.")

    st.caption("Evaluasi & insight otomatis ini update mengikuti kualitas data dan model terbaru.")
