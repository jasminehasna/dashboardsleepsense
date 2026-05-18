# Technical Report - SleepSense

Tanggal: 2026-05-18

## 1. Problem Discovery

SleepSense dikembangkan untuk membantu pengguna mengenali hubungan antara pola tidur, screen time, dan risiko stress awal. Latar belakang proyek menunjukkan bahwa durasi tidur yang kurang ideal dan penggunaan layar yang tinggi berpotensi berkaitan dengan kualitas tidur dan kesehatan mental.

Problem statement:

> Bagaimana teknologi dapat membantu pengguna mengenali pola tidur dan penggunaan layar, memperoleh deteksi dini risiko kesehatan mental, serta menerima rekomendasi edukatif secara personal?

Business question utama:

> Apakah screen time harian lebih dari 2 jam berkaitan dengan risiko stress sedang-berat?

## 2. Dataset

Dataset berasal dari Kaggle dan disimpan di `data/raw`.

| Dataset | Fungsi |
|---|---|
| Student Stress, Sleep & Screen Time Dataset | Analisis student/remaja |
| Sleep, Screen Time and Stress Analysis | Dataset utama model dan dashboard |
| Mental Wellness Tracker | Pendukung mood dan wellness |
| Sleep Health and Lifestyle Dataset | Pendukung lifestyle dan sleep health |
| Sleep Quality Dataset | Pendukung sleep quality dan kebiasaan tidur |

Dataset utama untuk model adalah `sleep_mobile_stress_dataset_15000.csv` karena memiliki 15.000 baris dan fitur inti paling lengkap.

## 3. Methodology

Pipeline:

```text
raw data -> preliminary assessment -> wrangling -> model-ready data -> feature engineering -> EDA -> dashboard
```

Script utama:

| Script | Fungsi |
|---|---|
| `scripts/preliminary_assessment.py` | Missing value, tipe data, duplikat, distribusi awal |
| `scripts/wrangle_datasets.py` | Standardisasi kolom, tipe data, satuan, cleaning |
| `scripts/feature_engineering.py` | Membuat fitur baru |
| `scripts/advanced_eda.py` | EDA lanjutan dan visual explanatory |
| `scripts/validate_model_data.py` | Validasi data model |
| `scripts/ab_testing.py` | A/B testing sederhana model klasifikasi |

## 4. Data Wrangling

Output:

| File | Baris | Kolom |
|---|---:|---:|
| `sleepsense_harmonized.csv` | 16674 | 36 |
| `sleepsense_model_ready.csv` | 15000 | 16 |
| `sleepsense_feature_engineered.csv` | 15000 | 32 |

Cleaning utama:

1. Standardisasi nama kolom.
2. Standardisasi satuan jam untuk durasi tidur dan screen time.
3. Mapping stress kategorikal ke skor numerik.
4. Mapping sleep quality kategorikal ke skor numerik.
5. Pembuatan age group.
6. Validasi missing value untuk dataset model-ready.

## 5. Feature Engineering

Fitur baru yang paling relevan:

| Fitur | Kegunaan |
|---|---|
| `sleep_debt_hours` | Mengukur kekurangan tidur dari kebutuhan ideal |
| `screen_ratio_before_bed` | Proporsi screen time yang terjadi sebelum tidur |
| `sleep_health_index` | Indeks gabungan durasi dan kualitas tidur |
| `digital_stimulation_index` | Indeks paparan digital |
| `recovery_balance_score` | Skor keseimbangan pemulihan |
| `screen_sleep_risk_score` | Skor risiko gabungan screen time dan tidur |

## 6. EDA dan Hasil Analisis

Business question dijawab melalui `reports/advanced_business_question_screen_time_stress.csv`.

| Screen time harian | Records | Stress risk rate | Rata-rata stress | Rata-rata sleep quality |
|---|---:|---:|---:|---:|
| `<= 2 jam/hari` | 1662 | 2.2% | 2.90 | 8.17 |
| `> 2 jam/hari` | 13338 | 70.9% | 7.49 | 6.01 |

Interpretasi:

Pengguna dengan screen time harian `> 2 jam` memiliki proporsi risiko stress sedang-berat yang lebih tinggi. Kelompok ini juga memiliki rata-rata sleep quality lebih rendah.

Risiko per kelompok usia:

| Kelompok usia | Records | Stress risk rate | Rata-rata screen time |
|---|---:|---:|---:|
| 13-18 | 338 | 62.4% | 5.64 |
| 19-35 | 6100 | 63.1% | 5.48 |
| 36-59 | 8562 | 63.5% | 5.51 |

## 7. Dashboard

Dashboard Streamlit berada di:

```text
dashboard.py
```

Fitur:

1. KPI utama.
2. Filter kelompok usia, gender, pekerjaan, kategori stress, dan screen time.
3. Visual explanatory business question.
4. Distribusi durasi tidur dan stress score.
5. Risiko per kelompok usia.
6. Pola tidur vs screen time.
7. Distribusi proxy DASS-21.

## 8. Model Readiness

Validasi data model dilakukan dengan:

```powershell
python scripts/validate_model_data.py
```

Kriteria validasi:

1. Semua required columns tersedia.
2. Tidak ada missing value pada fitur model.
3. Tipe data sesuai.
4. Nilai numerik berada pada rentang yang masuk akal.
5. Target `stress_risk` berbentuk binary.

Hasil validasi:

| Item | Nilai |
|---|---:|
| Rows | 15000 |
| Columns | 32 |
| Required columns | 20 |
| Missing required columns | 0 |
| Columns with missing values | 0 |
| Invalid type columns | 0 |
| Invalid range columns | 0 |
| Target positive rate | 63.3% |
| Status | PASS |

## 9. A/B Testing

A/B testing sederhana membandingkan:

| Eksperimen | Fitur |
|---|---|
| A | Core features |
| B | Core + engineered features |

Output:

```text
reports/ab_testing_results.csv
```

Metric yang digunakan:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Hasil A/B testing:

| Eksperimen | Feature count | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| A - Core features | 12 | 0.9417 | 0.9685 | 0.9384 | 0.9532 | 0.9896 |
| B - Core + engineered features | 18 | 0.9410 | 0.9679 | 0.9379 | 0.9527 | 0.9896 |

Interpretasi:

Kedua pendekatan memiliki performa sangat mirip. Feature engineered sedikit menaikkan ROC-AUC, tetapi baseline core features sedikit lebih tinggi pada accuracy, precision, recall, dan F1. Untuk model awal, core features sudah cukup kuat; fitur engineered tetap berguna untuk interpretasi dashboard dan eksperimen lanjutan.

## 10. Kesimpulan

1. Dataset utama siap digunakan untuk model awal.
2. Screen time harian tinggi berkaitan dengan risiko stress yang lebih tinggi secara deskriptif.
3. Fitur turunan seperti `sleep_debt_hours`, `digital_stimulation_index`, dan `screen_sleep_risk_score` dapat mendukung model AI Engineer.
4. Dashboard sudah dapat dipakai untuk menjelaskan insight utama kepada stakeholder.

## 11. Rekomendasi

1. Gunakan bahasa "screening awal" atau "indikasi risiko", bukan diagnosis.
2. Hitung DASS-21 asli dari jawaban kuesioner chatbot, bukan dari proxy dataset.
3. Lakukan uji statistik atau model lanjutan sebelum membuat klaim yang lebih kuat.
4. Jika memungkinkan, kumpulkan data pengguna Indonesia untuk validasi eksternal.
5. Deploy dashboard ke Streamlit Cloud setelah repository siap.
