from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "sleepsense_feature_engineered.csv"


st.set_page_config(
    page_title="SleepSense Dashboard",
    page_icon="S",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def percent(value: float) -> str:
    return f"{value:.1%}"


def metric_delta(current: float, baseline: float, suffix: str = "") -> str:
    delta = current - baseline
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.2f}{suffix}"


df = load_data()

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    [data-testid="stMetric"] {
        background: #f7f8f4;
        border: 1px solid #d9dfd1;
        padding: 0.9rem 1rem;
        border-radius: 8px;
    }
    .insight-box {
        background: #f4f7fb;
        border-left: 4px solid #245580;
        padding: 0.85rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0 1rem 0;
        color: #243447;
    }
    .warning-box {
        background: #fff8ed;
        border-left: 4px solid #b36b1f;
        padding: 0.85rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0 1rem 0;
        color: #3e2a14;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def insight(text: str, warning: bool = False) -> None:
    css_class = "warning-box" if warning else "insight-box"
    st.markdown(f"<div class='{css_class}'>{text}</div>", unsafe_allow_html=True)


st.title("SleepSense Dashboard")
st.caption("Analisis pola tidur, screen time, dan indikasi risiko stress berdasarkan dataset SleepSense.")

with st.sidebar:
    st.header("Filter")
    age_groups = st.multiselect(
        "Kelompok usia",
        options=sorted(df["age_group"].dropna().unique()),
        default=sorted(df["age_group"].dropna().unique()),
    )
    genders = st.multiselect(
        "Gender",
        options=sorted(df["gender"].dropna().unique()),
        default=sorted(df["gender"].dropna().unique()),
    )
    occupations = st.multiselect(
        "Occupation",
        options=sorted(df["occupation"].dropna().unique()),
        default=sorted(df["occupation"].dropna().unique()),
    )
    stress_categories = st.multiselect(
        "Kategori stress",
        options=["Low", "Mild", "Moderate", "High"],
        default=["Low", "Mild", "Moderate", "High"],
    )
    screen_range = st.slider(
        "Screen time harian",
        min_value=float(df["daily_screen_time_hours"].min()),
        max_value=float(df["daily_screen_time_hours"].max()),
        value=(
            float(df["daily_screen_time_hours"].min()),
            float(df["daily_screen_time_hours"].max()),
        ),
        step=0.1,
        format="%.1f jam",
    )
    st.caption("Gunakan filter untuk membandingkan segmen pengguna tanpa mengubah dataset asli.")

filtered = df[
    df["age_group"].isin(age_groups)
    & df["gender"].isin(genders)
    & df["occupation"].isin(occupations)
    & df["stress_category"].isin(stress_categories)
    & df["daily_screen_time_hours"].between(screen_range[0], screen_range[1])
].copy()

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini.")
    st.stop()

baseline_stress_rate = df["stress_risk"].mean()
current_stress_rate = filtered["stress_risk"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Record", f"{len(filtered):,}")
col2.metric("Stress risk", percent(current_stress_rate), metric_delta(current_stress_rate, baseline_stress_rate))
col3.metric("Rata-rata tidur", f"{filtered['sleep_duration_hours'].mean():.2f} jam")
col4.metric("Rata-rata screen time", f"{filtered['daily_screen_time_hours'].mean():.2f} jam")

insight(
    f"Pada data terfilter, {percent(current_stress_rate)} record masuk kategori stress sedang-berat. "
    f"Rata-rata durasi tidur adalah {filtered['sleep_duration_hours'].mean():.2f} jam dan rata-rata screen time harian "
    f"{filtered['daily_screen_time_hours'].mean():.2f} jam."
)

st.divider()

st.subheader("Jawaban Business Question")
st.caption("Apakah screen time harian lebih dari 2 jam berkaitan dengan risiko stress sedang-berat?")

bq = (
    filtered.assign(screen_group=filtered["daily_screen_time_hours"].gt(2).map({True: "> 2 jam/hari", False: "<= 2 jam/hari"}))
    .groupby("screen_group", observed=True)
    .agg(
        records=("stress_risk", "size"),
        stress_risk_rate=("stress_risk", "mean"),
        avg_stress_score=("stress_score", "mean"),
        avg_sleep_quality=("sleep_quality_score", "mean"),
        avg_sleep_debt=("sleep_debt_hours", "mean"),
    )
    .reset_index()
)

if set(bq["screen_group"]) == {"<= 2 jam/hari", "> 2 jam/hari"}:
    low_rate = float(bq.loc[bq["screen_group"].eq("<= 2 jam/hari"), "stress_risk_rate"].iloc[0])
    high_rate = float(bq.loc[bq["screen_group"].eq("> 2 jam/hari"), "stress_risk_rate"].iloc[0])
    insight(
        f"Kelompok screen time > 2 jam/hari memiliki stress risk {percent(high_rate)}, "
        f"sedangkan kelompok <= 2 jam/hari {percent(low_rate)}. Visual ini langsung menjawab business question utama."
    )
else:
    insight(
        "Filter saat ini hanya menyisakan satu kelompok screen time, sehingga perbandingan business question belum bisa terlihat.",
        warning=True,
    )

left, right = st.columns([1.05, 1])
with left:
    bar = (
        alt.Chart(bq)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("screen_group:N", title="Screen time harian"),
            y=alt.Y("stress_risk_rate:Q", title="Proporsi stress risk", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("screen_group:N", legend=None, scale=alt.Scale(range=["#245580", "#7f3c2d"])),
            tooltip=[
                "screen_group",
                "records",
                alt.Tooltip("stress_risk_rate:Q", format=".1%"),
                alt.Tooltip("avg_stress_score:Q", format=".2f"),
                alt.Tooltip("avg_sleep_quality:Q", format=".2f"),
            ],
        )
        .properties(height=330)
    )
    st.altair_chart(bar, use_container_width=True)
with right:
    st.dataframe(
        bq.assign(stress_risk_rate=bq["stress_risk_rate"].map(lambda value: f"{value:.1%}")),
        use_container_width=True,
        hide_index=True,
    )

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Distribusi", "Kelompok Usia", "Pola Tidur vs Screen Time", "DASS-21 Proxy"]
)

with tab1:
    insight(
        "Distribusi ini membantu melihat apakah pola tidur dan stress cenderung terkonsentrasi pada rentang tertentu. "
        "Sebaran stress yang condong ke skor tinggi perlu diperhatikan saat menyusun rekomendasi chatbot."
    )
    col_a, col_b = st.columns(2)
    with col_a:
        sleep_hist = (
            alt.Chart(filtered)
            .mark_bar()
            .encode(
                x=alt.X("sleep_duration_hours:Q", bin=alt.Bin(maxbins=28), title="Durasi tidur (jam)"),
                y=alt.Y("count():Q", title="Jumlah record"),
                color=alt.value("#2f5d31"),
                tooltip=["count()"],
            )
            .properties(title="Distribusi Durasi Tidur", height=320)
        )
        st.altair_chart(sleep_hist, use_container_width=True)
    with col_b:
        stress_hist = (
            alt.Chart(filtered)
            .mark_bar()
            .encode(
                x=alt.X("stress_score:Q", bin=alt.Bin(maxbins=20), title="Stress score"),
                y=alt.Y("count():Q", title="Jumlah record"),
                color=alt.value("#7f3c2d"),
                tooltip=["count()"],
            )
            .properties(title="Distribusi Stress Score", height=320)
        )
        st.altair_chart(stress_hist, use_container_width=True)

with tab2:
    age_summary = (
        filtered.groupby("age_group", observed=True)
        .agg(
            records=("stress_risk", "size"),
            stress_risk_rate=("stress_risk", "mean"),
            avg_sleep_duration=("sleep_duration_hours", "mean"),
            avg_screen_time=("daily_screen_time_hours", "mean"),
            avg_sleep_debt=("sleep_debt_hours", "mean"),
        )
        .reset_index()
    )
    if not age_summary.empty:
        top_age = age_summary.sort_values("stress_risk_rate", ascending=False).iloc[0]
        insight(
            f"Kelompok usia dengan stress risk tertinggi pada filter ini adalah {top_age['age_group']} "
            f"dengan proporsi {percent(float(top_age['stress_risk_rate']))}."
        )
    age_chart = (
        alt.Chart(age_summary)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("age_group:N", title="Kelompok usia", sort=["13-18", "19-35", "36-59", "60+"]),
            y=alt.Y("stress_risk_rate:Q", title="Proporsi stress risk", scale=alt.Scale(domain=[0, 1])),
            color=alt.value("#2f5d31"),
            tooltip=[
                "age_group",
                "records",
                alt.Tooltip("stress_risk_rate:Q", format=".1%"),
                alt.Tooltip("avg_sleep_duration:Q", format=".2f"),
                alt.Tooltip("avg_screen_time:Q", format=".2f"),
                alt.Tooltip("avg_sleep_debt:Q", format=".2f"),
            ],
        )
        .properties(height=360)
    )
    st.altair_chart(age_chart, use_container_width=True)
    st.dataframe(age_summary, use_container_width=True, hide_index=True)

with tab3:
    insight(
        "Scatter plot ini memperlihatkan hubungan pola tidur dan screen time pada level record. "
        "Warna kategori stress membantu melihat area dengan konsentrasi risiko lebih tinggi."
    )
    scatter = (
        alt.Chart(filtered.sample(min(len(filtered), 5000), random_state=42))
        .mark_circle(size=45, opacity=0.45)
        .encode(
            x=alt.X("daily_screen_time_hours:Q", title="Screen time harian (jam)"),
            y=alt.Y("sleep_duration_hours:Q", title="Durasi tidur (jam)"),
            color=alt.Color("stress_category:N", title="Kategori stress"),
            tooltip=[
                "age",
                "age_group",
                "gender",
                "occupation",
                alt.Tooltip("daily_screen_time_hours:Q", format=".2f"),
                alt.Tooltip("sleep_duration_hours:Q", format=".2f"),
                alt.Tooltip("stress_score:Q", format=".2f"),
                "stress_category",
            ],
        )
        .properties(height=420)
    )
    st.altair_chart(scatter, use_container_width=True)

with tab4:
    insight(
        "Skor ini adalah proxy dari stress_score dataset, bukan hasil kuesioner DASS-21 asli. "
        "Untuk produk akhir, skor DASS-21 harus dihitung dari jawaban 21 item kuesioner.",
        warning=True,
    )
    dass = (
        filtered.groupby("dass21_stress_proxy_category", observed=True)
        .agg(
            records=("stress_risk", "size"),
            avg_stress_score=("stress_score", "mean"),
            avg_screen_time=("daily_screen_time_hours", "mean"),
            avg_sleep_quality=("sleep_quality_score", "mean"),
        )
        .reindex(["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"])
        .dropna(how="all")
        .reset_index()
    )
    dass_chart = (
        alt.Chart(dass)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("dass21_stress_proxy_category:N", title="Kategori proxy DASS-21", sort=["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]),
            y=alt.Y("records:Q", title="Jumlah record"),
            color=alt.value("#245580"),
            tooltip=[
                "dass21_stress_proxy_category",
                "records",
                alt.Tooltip("avg_stress_score:Q", format=".2f"),
                alt.Tooltip("avg_screen_time:Q", format=".2f"),
                alt.Tooltip("avg_sleep_quality:Q", format=".2f"),
            ],
        )
        .properties(height=360)
    )
    st.altair_chart(dass_chart, use_container_width=True)
    st.dataframe(dass, use_container_width=True, hide_index=True)

st.divider()

with st.expander("Data hasil filter"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
