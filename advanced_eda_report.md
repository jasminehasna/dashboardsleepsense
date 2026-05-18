# Advanced EDA Report - SleepSense

Tanggal: 2026-05-18

## Tujuan

Menyelesaikan EDA lanjutan untuk menjawab kebutuhan pekan ini:

1. Heatmap korelasi.
2. Distribusi risiko per kelompok usia.
3. Pola tidur vs screen time.
4. Distribusi skor DASS-21.
5. Visualisasi explanatory yang menjawab business question secara langsung.

## Dataset Analisis

File utama:

```text
data/processed/sleepsense_feature_engineered.csv
```

Jumlah data:

| Dataset | Baris | Kolom |
|---|---:|---:|
| Feature-engineered dataset | 15000 | 32 |

Dataset ini berasal dari `sleepsense_model_ready.csv` dan ditambah fitur turunan untuk EDA dan model awal.

## Catatan DASS-21

Dataset Kaggle yang digunakan tidak memuat jawaban item DASS-21 asli. Karena itu, visualisasi DASS-21 pada EDA ini menggunakan:

```text
dass21_stress_proxy_score
```

Fitur tersebut adalah proxy berbasis `stress_score`, bukan hasil kuesioner DASS-21 klinis. Untuk aplikasi chatbot, skor DASS-21 asli tetap harus dihitung dari jawaban 21 item kuesioner.

## Feature Engineering

Script:

```powershell
python scripts/feature_engineering.py
```

Fitur baru:

| Fitur | Deskripsi |
|---|---|
| `sleep_debt_hours` | Selisih durasi tidur ideal dan durasi tidur aktual |
| `screen_ratio_before_bed` | Proporsi screen time harian yang terjadi sebelum tidur |
| `high_daily_screen_time` | True jika screen time harian `> 2 jam` |
| `high_before_bed_screen_time` | True jika screen time sebelum tidur `> 1 jam` |
| `short_sleep` | True jika durasi tidur `< 7 jam` |
| `poor_sleep_quality` | True jika sleep quality `< 6` |
| `stress_category` | Low, Mild, Moderate, High |
| `dass21_stress_proxy_score` | Proxy skor stress skala 0-42 |
| `dass21_stress_proxy_category` | Normal, Mild, Moderate, Severe, Extremely Severe |
| `sleep_health_index` | Indeks gabungan durasi dan kualitas tidur |
| `digital_stimulation_index` | Indeks paparan digital dari screen time, pre-sleep screen time, dan notifikasi |
| `recovery_balance_score` | Skor keseimbangan pemulihan |
| `screen_sleep_risk_score` | Skor risiko gabungan sleep debt, screen time, dan kualitas tidur buruk |

## Output EDA Lanjutan

Script:

```powershell
python scripts/advanced_eda.py
```

File report:

| File | Isi |
|---|---|
| `reports/advanced_correlation_matrix.csv` | Matriks korelasi fitur asli dan fitur turunan |
| `reports/advanced_risk_by_age_group.csv` | Risiko stress per kelompok usia |
| `reports/advanced_sleep_vs_screen_time.csv` | Pola durasi tidur vs screen time |
| `reports/advanced_dass21_proxy_distribution.csv` | Distribusi kategori proxy DASS-21 |
| `reports/advanced_business_question_screen_time_stress.csv` | Jawaban langsung business question |

Grafik:

| Grafik | File |
|---|---|
| Heatmap korelasi | `reports/figures/advanced_correlation_heatmap.png` |
| Risiko per kelompok usia | `reports/figures/advanced_risk_by_age_group.png` |
| Pola tidur vs screen time heatmap | `reports/figures/advanced_sleep_vs_screen_time_heatmap.png` |
| Pola tidur vs screen time scatter | `reports/figures/advanced_sleep_vs_screen_time_scatter.png` |
| Distribusi proxy DASS-21 | `reports/figures/advanced_dass21_proxy_distribution.png` |
| Business question explanatory | `reports/figures/advanced_business_question_screen_time_stress.png` |

## Jawaban Business Question

Business question:

> Apakah screen time harian lebih dari 2 jam berkaitan dengan risiko stress sedang-berat?

Hasil:

| Screen time harian | Records | Stress risk rate | Rata-rata stress | Rata-rata sleep quality | Rata-rata screen-sleep risk |
|---|---:|---:|---:|---:|---:|
| `<= 2 jam/hari` | 1662 | 2.2% | 2.90 | 8.17 | 5.62 |
| `> 2 jam/hari` | 13338 | 70.9% | 7.49 | 6.01 | 10.20 |

Interpretasi:

Kelompok dengan screen time harian `> 2 jam` memiliki proporsi stress sedang-berat jauh lebih tinggi daripada kelompok `<= 2 jam`. Perbedaan ini juga terlihat pada rata-rata stress score, sleep quality, dan screen-sleep risk score.

Catatan: hasil ini bersifat deskriptif, bukan bukti kausal.

## Risiko per Kelompok Usia

| Kelompok usia | Records | Stress risk rate | Rata-rata stress | Rata-rata sleep debt | Rata-rata screen time |
|---|---:|---:|---:|---:|---:|
| 13-18 | 338 | 62.4% | 7.05 | 2.02 | 5.64 |
| 19-35 | 6100 | 63.1% | 6.97 | 1.58 | 5.48 |
| 36-59 | 8562 | 63.5% | 6.98 | 1.60 | 5.51 |

Risiko stress relatif tinggi di semua kelompok usia yang tersedia pada dataset utama. Tidak ada kelompok 60+ pada model-ready dataset.

## Distribusi Proxy DASS-21

| Kategori proxy | Records | Rata-rata stress | Rata-rata screen time | Rata-rata sleep quality |
|---|---:|---:|---:|---:|
| Normal | 2734 | 2.65 | 2.25 | 8.42 |
| Mild | 1164 | 4.45 | 3.20 | 7.62 |
| Moderate | 2117 | 5.61 | 4.03 | 7.05 |
| Severe | 2430 | 7.21 | 5.31 | 6.32 |
| Extremely Severe | 6555 | 9.59 | 7.81 | 4.81 |

Pola awalnya konsisten: semakin tinggi kategori proxy stress, rata-rata screen time meningkat dan rata-rata sleep quality menurun.
