# Streamlit Cloud Deployment Checklist

Tanggal: 2026-05-18

## File yang Dibutuhkan

Pastikan file berikut ada di repository yang akan dihubungkan ke Streamlit Cloud:

| File | Status |
|---|---|
| `dashboard.py` | Aplikasi utama Streamlit |
| `requirements.txt` | Dependency Python |
| `data/processed/sleepsense_feature_engineered.csv` | Dataset dashboard |
| `docs/pipeline_documentation.md` | Dokumentasi pipeline |

## Cara Deploy

1. Push folder `capstone` ke GitHub repository.
2. Buka Streamlit Cloud.
3. Pilih repository project.
4. Set main file path:

```text
dashboard.py
```

5. Deploy.
6. Uji akses publik dari browser atau jaringan lain.

## Checklist Uji Akses

| Check | Kriteria |
|---|---|
| App terbuka | Halaman dashboard tampil tanpa error |
| Dataset terbaca | KPI record menampilkan 15.000 record saat filter default |
| Filter berjalan | Age group, gender, occupation, stress category, dan screen time bisa mengubah grafik |
| Grafik responsif | Chart menyesuaikan lebar layar |
| Narasi muncul | Insight text tampil di setiap section |
| DASS-21 proxy disclaimer | Catatan proxy DASS-21 terlihat |

## Catatan

Deploy publik belum dilakukan dari sesi ini karena membutuhkan akses akun Streamlit Cloud/GitHub. Dashboard sudah siap dijalankan lokal dan siap dipush ke repository.
