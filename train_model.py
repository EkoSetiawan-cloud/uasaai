# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import numpy as np

# 1. Load data
data_path = "data/simulasi_kasus_darurat.csv"
df = pd.read_csv(data_path)

# 2. Drop baris yang targetnya NaN/kosong ("Hasil Penanganan" harus sudah terisi!)
df = df.dropna(subset=["Hasil Penanganan"])

# 3. Preprocessing: One-hot encoding untuk kolom kategori
kategorik = ["Jenis Insiden", "Tingkat Keparahan", "Tindakan Awal", "Lokasi Kejadian"]
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded = encoder.fit_transform(df[kategorik])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(kategorik))

# Kolom numerik
num_cols = ["Jumlah Korban", "Waktu Respons Petugas (menit)"]
X_num = df[num_cols].reset_index(drop=True)

# Gabungkan fitur akhir
X = pd.concat([encoded_df, X_num], axis=1)
y_klasifikasi = df["Hasil Penanganan"].reset_index(drop=True)
y_regresi = df["Waktu Respons Petugas (menit)"].reset_index(drop=True)

# 4. Pastikan TIDAK ada NaN di fitur maupun target
X = X.dropna()
y_klasifikasi = y_klasifikasi[X.index]
y_regresi = y_regresi[X.index]

# 5. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_klasifikasi, test_size=0.2, random_state=42)

# 6. Training Random Forest (klasifikasi)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 7. Training Linear Regression (regresi)
reg_model = LinearRegression()
reg_model.fit(X_train, y_regresi[X_train.index])

# 8. Simpan model ke folder /models/
os.makedirs("models", exist_ok=True)
joblib.dump(rf_model, "models/rf_model.pkl")
joblib.dump(reg_model, "models/regression_model.pkl")
joblib.dump(encoder, "models/encoder.pkl")  # Simpan encoder untuk prediksi real-time

print("Model berhasil disimpan ke folder /models/")

# --- EVALUASI KLASIFIKASI ---
y_pred_cls = rf_model.predict(X_test)
print("\n==== Evaluasi Random Forest (Klasifikasi Hasil Penanganan) ====")
print(f"Akurasi: {accuracy_score(y_test, y_pred_cls):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_cls))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_cls))

# --- EVALUASI REGRESI ---
y_test_reg = y_regresi[X_test.index]
y_pred_reg = reg_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))
print("\n==== Evaluasi Linear Regression (Prediksi Waktu Respons) ====")
print(f"R2 Score: {r2_score(y_test_reg, y_pred_reg):.2f}")
print(f"MAE: {mean_absolute_error(y_test_reg, y_pred_reg):.2f}")
print(f"RMSE: {rmse:.2f}")
