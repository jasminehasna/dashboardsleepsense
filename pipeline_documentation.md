# SleepSense Data Pipeline

Tanggal: 2026-05-18

## Ringkasan Pipeline

Pipeline data SleepSense berjalan dari raw dataset menuju cleaned, model-ready, feature-engineered, EDA report, dan dashboard.

```text
data/raw/*.csv
    -> scripts/preliminary_assessment.py
    -> scripts/wrangle_datasets.py
    -> data/processed/sleepsense_model_ready.csv
    -> scripts/feature_engineering.py
    -> data/processed/sleepsense_feature_engineered.csv
    -> scripts/advanced_eda.py
    -> reports/*.csv + reports/figures/*.png
    -> scripts/validate_model_data.py
    -> scripts/ab_testing.py
    -> dashboard.py
```

## 1. Raw Data

Folder:

```text
data/raw
```

Isi:

| File | Fungsi |
|---|---|
| `sleep_mobile_stress_dataset_15000.csv` | Dataset utama model dan EDA |
| `mental_wellness_test.csv` | Dataset pendukung mood/wellness |
| `Sleep_health_and_lifestyle_dataset.csv` | Dataset pendukung lifestyle |
| `Sleep_Quality_Dataset.csv` | Dataset pendukung sleep quality |
| `student_stress_sleep_screen.csv` | Dataset pendukung student segment |

## 2. Preliminary Assessment

Script:

```powershell
python scripts/preliminary_assessment.py
```

Output:

| Output | Fungsi |
|---|---|
| `reports/preliminary_assessment_summary.csv` | Ringkasan missing value, tipe data, duplikat |
| `reports/column_dictionary_draft.csv` | Draft data dictionary dari kolom aktual |
| `reports/figures/*_distribution.png` | Distribusi awal setiap dataset |

## 3. Wrangling dan Cleaning

Script:

```powershell
python scripts/wrangle_datasets.py
```

Output:

| Output | Fungsi |
|---|---|
| `data/processed/sleepsense_harmonized.csv` | Gabungan semua dataset dengan kolom standar |
| `data/processed/sleepsense_model_ready.csv` | Dataset strict untuk AI Engineer, tanpa missing pada fitur training awal |
| `reports/wrangling_cleaning_summary.csv` | Ringkasan cleaning |
| `reports/wrangling_outlier_summary.csv` | Ringkasan outlier |

Catatan:

`sleepsense_harmonized.csv` boleh memiliki sel kosong karena menggabungkan dataset dengan struktur berbeda. Untuk model, gunakan `sleepsense_model_ready.csv`.

## 4. Feature Engineering

Script:

```powershell
python scripts/feature_engineering.py
```

Output:

| Output | Fungsi |
|---|---|
| `data/processed/sleepsense_feature_engineered.csv` | Dataset utama dashboard, EDA lanjutan, dan eksperimen model |
| `reports/feature_engineering_summary.csv` | Ringkasan fitur turunan |

Fitur baru utama:

- `sleep_debt_hours`
- `screen_ratio_before_bed`
- `stress_category`
- `dass21_stress_proxy_score`
- `dass21_stress_proxy_category`
- `sleep_health_index`
- `digital_stimulation_index`
- `recovery_balance_score`
- `screen_sleep_risk_score`

## 5. Advanced EDA

Script:

```powershell
python scripts/advanced_eda.py
```

Output:

| Output | Fungsi |
|---|---|
| `reports/advanced_correlation_matrix.csv` | Heatmap korelasi |
| `reports/advanced_risk_by_age_group.csv` | Risiko per kelompok usia |
| `reports/advanced_sleep_vs_screen_time.csv` | Pola tidur vs screen time |
| `reports/advanced_dass21_proxy_distribution.csv` | Distribusi proxy DASS-21 |
| `reports/advanced_business_question_screen_time_stress.csv` | Visualisasi explanatory business question |

## 6. Model Validation

Script:

```powershell
python scripts/validate_model_data.py
```

Output:

| Output | Fungsi |
|---|---|
| `reports/model_data_validation_report.csv` | Validasi kolom, tipe data, missing value, dan rentang nilai |
| `reports/model_data_validation_summary.json` | Ringkasan status kesiapan data model |

Status terakhir: `PASS`.

## 7. A/B Testing

Script:

```powershell
python scripts/ab_testing.py
```

Output:

| Output | Fungsi |
|---|---|
| `reports/ab_testing_results.csv` | Perbandingan model core features vs engineered features |

Eksperimen:

1. `A_baseline_core_features`
2. `B_engineered_features`

## 8. Dashboard Streamlit

File:

```text
dashboard.py
```

Menjalankan dashboard:

```powershell
streamlit run dashboard.py
```

Dashboard membaca:

```text
data/processed/sleepsense_feature_engineered.csv
```

Fitur dashboard:

- Main insight business question.
- Filter kelompok usia, gender, occupation, kategori stress, dan screen time.
- Distribusi durasi tidur dan stress score.
- Risiko stress per kelompok usia.
- Pola tidur vs screen time.
- Distribusi proxy DASS-21.

## Catatan Penting

1. Proxy DASS-21 bukan hasil kuesioner DASS-21 asli.
2. Untuk chatbot, DASS-21 harus dihitung dari jawaban item kuesioner.
3. Output model dan dashboard harus disebut screening awal atau indikasi risiko, bukan diagnosis.
