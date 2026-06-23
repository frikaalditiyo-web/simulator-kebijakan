import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

# ─────────────────────────────────────────────
# PAGE CONFIG (harus paling atas sebelum st lain)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Policy Simulator | Frika Alditiyo",
    page_icon="🧠",
    layout="wide"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Background utama */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Header brand */
    .brand-header {
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
        border-radius: 12px;
        padding: 20px 28px;
        margin-bottom: 24px;
    }
    .brand-header h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .brand-header p {
        color: #cdd9e5;
        font-size: 0.85rem;
        margin: 4px 0 0 0;
    }

    /* Card hasil */
    .result-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }

    /* Delta positif / negatif */
    .delta-positive { color: #3fb950; font-weight: 700; font-size: 1.1rem; }
    .delta-negative { color: #f85149; font-weight: 700; font-size: 1.1rem; }
    .delta-neutral   { color: #8b949e; font-weight: 700; font-size: 1.1rem; }

    /* Metric override */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetricLabel"] { color: #8b949e !important; }
    [data-testid="stMetricValue"] { color: #e6edf3 !important; }

    /* Slider label */
    .stSlider label { color: #cdd9e5 !important; }

    /* Footer */
    .footer {
        text-align: center;
        color: #484f58;
        font-size: 0.75rem;
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #21262d;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODEL — Train
# ─────────────────────────────────────────────
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
y_train = np.array([50, 80, 110, 90, 150])
model   = LinearRegression().fit(X_train, y_train)

baseline_input = np.array([[10, 10]])
baseline_pred  = model.predict(baseline_input)[0]

def run_simulation(new_iklan, new_diskon):
    pred    = model.predict(np.array([[new_iklan, new_diskon]]))[0]
    delta_y = pred - baseline_pred
    return pred, delta_y

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px 0;'>
        <div style='font-size:3rem;'>🧠</div>
        <div style='color:#388bfd; font-weight:700; font-size:1rem;'>Frika Alditiyo</div>
        <div style='color:#8b949e; font-size:0.75rem;'>2313020008</div>
    </div>
    <hr style='border-color:#30363d; margin: 12px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎛️ Tuas Kebijakan")
    iklan_slider  = st.slider("📢 Anggaran Iklan (Juta Rp)", 0, 50, 10)
    diskon_slider = st.slider("🏷️ Besaran Diskon (%)", 0, 50, 10)

    st.markdown("<hr style='border-color:#30363d;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#8b949e; font-size:0.78rem; line-height:1.6;'>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER BRAND
# ─────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <h1> Kebijakan Keuntungan Toko</h1>
    <p>Frika Alditiyo &nbsp;·&nbsp; NPM 2313020008 &nbsp;·&nbsp; Informatika — UNP Kediri &nbsp;·&nbsp; Praktikum Pemodelan & Simulasi Minggu 14</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

# ─────────────────────────────────────────────
# METRIK
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("📦 Baseline Keuntungan",  f"Rp {baseline_pred:.2f} Jt")
col2.metric("🚀 Prediksi Intervensi",  f"Rp {hasil_pred:.2f} Jt")
col3.metric("📊 Delta (Selisih)",       f"Rp {delta:.2f} Jt",
            delta=f"{delta:.2f} Jt")

# ─────────────────────────────────────────────
# NARASI OTOMATIS
# ─────────────────────────────────────────────
if delta > 0:
    st.success(f"✅ **Keputusan Baik!** Skenario ini meningkatkan keuntungan sebesar **Rp {delta:.2f} Juta** dibanding kondisi saat ini.")
elif delta < 0:
    st.error(f"⚠️ **Perhatian!** Skenario ini menurunkan keuntungan sebesar **Rp {abs(delta):.2f} Juta**. Pertimbangkan ulang kebijakan ini.")
else:
    st.info("ℹ️ Skenario ini menghasilkan keuntungan yang sama dengan baseline. Tidak ada perubahan signifikan.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VISUALISASI
# ─────────────────────────────────────────────
col_chart, col_tabel = st.columns([3, 2])

with col_chart:
    st.markdown("#### 📊 Perbandingan Skenario")
    data_plot = pd.DataFrame({
        'Skenario': ['Baseline', 'Intervensi'],
        'Keuntungan (Juta)': [round(baseline_pred, 2), round(hasil_pred, 2)]
    })
    st.bar_chart(data=data_plot, x='Skenario', y='Keuntungan (Juta)', height=300)

with col_tabel:
    st.markdown("#### 📋 Ringkasan Input")
    df_summary = pd.DataFrame({
        'Variabel'   : ['Anggaran Iklan', 'Besaran Diskon'],
        'Baseline'   : ['Rp 10 Jt', '10%'],
        'Intervensi' : [f'Rp {iklan_slider} Jt', f'{diskon_slider}%'],
        'Selisih'    : [f'{iklan_slider - 10:+} Jt', f'{diskon_slider - 10:+}%']
    })
    st.dataframe(df_summary, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-card">
        <div style='color:#8b949e; font-size:0.8rem;'>Model Info</div>
        <div style='color:#cdd9e5; font-size:0.85rem; margin-top:6px;'>
            📌 Algoritma: <b>Linear Regression</b><br>
            📌 Fitur: Iklan, Diskon<br>
            📌 Koefisien Iklan: <b>{model.coef_[0]:.4f}</b><br>
            📌 Koefisien Diskon: <b>{model.coef_[1]:.4f}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SENSITIVITY SWEEP
# ─────────────────────────────────────────────
st.markdown("#### 🔍 Analisis Sensitivitas — Sweep Variabel")

col_s1, col_s2 = st.columns(2)

with col_s1:
    sweep_iklan = np.arange(0, 51, 1)
    pred_iklan  = [model.predict(np.array([[i, diskon_slider]]))[0] for i in sweep_iklan]
    df_iklan    = pd.DataFrame({'Anggaran Iklan (Juta)': sweep_iklan, 'Prediksi Keuntungan': pred_iklan})
    st.caption("Efek perubahan Iklan (Diskon tetap)")
    st.line_chart(df_iklan, x='Anggaran Iklan (Juta)', y='Prediksi Keuntungan', height=220)

with col_s2:
    sweep_diskon = np.arange(0, 51, 1)
    pred_diskon  = [model.predict(np.array([[iklan_slider, d]]))[0] for d in sweep_diskon]
    df_diskon    = pd.DataFrame({'Besaran Diskon (%)': sweep_diskon, 'Prediksi Keuntungan': pred_diskon})
    st.caption("Efek perubahan Diskon (Iklan tetap)")
    st.line_chart(df_diskon, x='Besaran Diskon (%)', y='Prediksi Keuntungan', height=220)

# ─────────────────────────────────────────────
# KESIMPULAN WHAT-IF
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 📝 Kesimpulan Analisis What-If")

# Tentukan variabel mana yang paling berpengaruh
koef_iklan  = abs(model.coef_[0])
koef_diskon = abs(model.coef_[1])
variabel_dominan = "Anggaran Iklan" if koef_iklan > koef_diskon else "Besaran Diskon"

# Tentukan status skenario
if delta > 5:
    status      = "sangat menguntungkan"
    rekomendasi = "Skenario ini <b>layak diterapkan</b>. Pertahankan kombinasi kebijakan ini."
elif delta > 0:
    status      = "sedikit menguntungkan"
    rekomendasi = "Skenario ini memberikan hasil positif namun <b>belum signifikan</b>. Coba naikkan anggaran iklan lebih lanjut."
elif delta == 0:
    status      = "netral"
    rekomendasi = "Tidak ada perubahan berarti. <b>Coba ubah salah satu variabel</b> untuk melihat dampaknya."
elif delta > -5:
    status      = "sedikit merugikan"
    rekomendasi = "Skenario ini <b>kurang disarankan</b>. Pertimbangkan untuk mengurangi besaran diskon."
else:
    status      = "sangat merugikan"
    rekomendasi = "Skenario ini <b>tidak disarankan</b>. Kembali ke kondisi baseline atau cari kombinasi lain."

st.markdown(f"""
<div style='background-color:#161b22; border:1px solid #30363d; border-left: 4px solid #388bfd;
            border-radius:10px; padding:20px 24px; margin-top:8px;'>
    <p style='color:#8b949e; font-size:0.8rem; margin:0 0 10px 0;'>HASIL SIMULASI WHAT-IF</p>
    <p style='color:#e6edf3; margin:0 0 8px 0;'>
        Dengan <b style='color:#388bfd;'>Iklan = Rp {iklan_slider} Juta</b> dan
        <b style='color:#388bfd;'>Diskon = {diskon_slider}%</b>,
        skenario ini dinilai <b style='color:#f0a500;'>{status}</b>
        dengan perubahan keuntungan sebesar
        <b style='color:{"#3fb950" if delta >= 0 else "#f85149"};'>Rp {delta:.2f} Juta</b>
        dari kondisi baseline.
    </p>
    <p style='color:#e6edf3; margin:0 0 8px 0;'>
        Variabel paling sensitif (dominan) adalah
        <b style='color:#388bfd;'>{variabel_dominan}</b>
        dengan koefisien <b style='color:#388bfd;'>{max(koef_iklan, koef_diskon):.4f}</b> —
        artinya setiap kenaikan 1 unit pada variabel ini memberikan dampak terbesar terhadap keuntungan.
    </p>
    <p style='color:#cdd9e5; margin:0;'>💡 <b>Rekomendasi:</b> {rekomendasi}</p>
</div>
""", unsafe_allow_html=True)