import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import streamlit as st


st.set_page_config(
    page_title="Policy Simulator | Frika Alditiyo",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
<style>
    :root {
        --track: #090b10;
        --panel: #111722;
        --panel-2: #171f2d;
        --line: #2a3547;
        --text: #f2f6fb;
        --muted: #9aa8b8;
        --red: #ff2f45;
        --yellow: #f7c843;
        --green: #25d366;
        --cyan: #38d5ff;
    }

    .stApp {
        background:
            linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px) 0 0 / 42px 42px,
            radial-gradient(circle at 18% 8%, rgba(255,47,69,0.18), transparent 32%),
            radial-gradient(circle at 85% 15%, rgba(56,213,255,0.12), transparent 30%),
            #090b10;
        color: var(--text);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c111a 0%, #111722 100%);
        border-right: 1px solid var(--line);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4, p, label, span, div {
        letter-spacing: 0 !important;
    }

    .race-hero {
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 28px 30px;
        margin-bottom: 18px;
        background:
            linear-gradient(135deg, rgba(255,47,69,0.26) 0%, rgba(17,23,34,0.94) 42%, rgba(56,213,255,0.16) 100%);
    }

    .race-hero:before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(45deg, rgba(255,255,255,0.08) 25%, transparent 25% 50%, rgba(255,255,255,0.08) 50% 75%, transparent 75%) 0 0 / 28px 28px;
        opacity: 0.18;
        pointer-events: none;
    }

    .race-hero h1 {
        position: relative;
        color: var(--text);
        font-size: clamp(2rem, 5vw, 4.3rem);
        font-weight: 900;
        line-height: 0.95;
        margin: 0;
        text-transform: uppercase;
    }

    .race-hero p {
        position: relative;
        max-width: 920px;
        color: #d8e3ef;
        font-size: 0.98rem;
        margin: 14px 0 0 0;
    }

    .race-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin: 6px 0 18px 0;
    }

    .race-tile,
    .result-card,
    .strategy-card,
    .gauge-card {
        background: linear-gradient(180deg, rgba(23,31,45,0.96), rgba(13,18,27,0.96));
        border: 1px solid var(--line);
        border-radius: 10px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.22);
    }

    .race-tile {
        padding: 14px 16px;
        min-height: 86px;
    }

    .tile-label {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .tile-value {
        color: var(--text);
        font-size: 1.45rem;
        font-weight: 900;
        margin-top: 8px;
    }

    .tile-sub {
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 4px;
    }

    .status-badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        color: #0b1018;
        background: var(--yellow);
        font-size: 0.74rem;
        font-weight: 900;
        text-transform: uppercase;
    }

    .result-card,
    .strategy-card,
    .gauge-card {
        padding: 18px 20px;
        margin-bottom: 16px;
    }

    .card-title {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 900;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .speedbar {
        height: 14px;
        overflow: hidden;
        background: #202a39;
        border: 1px solid #334155;
        border-radius: 999px;
    }

    .speedbar-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--red), var(--yellow), var(--green));
    }

    .policy-map {
        height: 210px;
        position: relative;
        border-radius: 12px;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px) 0 0 / 25% 100%,
            linear-gradient(0deg, rgba(255,255,255,0.08) 1px, transparent 1px) 0 0 / 100% 25%,
            radial-gradient(circle at var(--point-x) var(--point-y), rgba(255,47,69,0.28), transparent 18%),
            linear-gradient(135deg, rgba(255,47,69,0.12), rgba(56,213,255,0.10)),
            #101725;
        border: 1px solid var(--line);
        overflow: hidden;
    }

    .policy-map:before,
    .policy-map:after {
        content: "";
        position: absolute;
        background: rgba(242,246,251,0.28);
    }

    .policy-map:before {
        left: 50%;
        top: 12px;
        bottom: 28px;
        width: 1px;
    }

    .policy-map:after {
        left: 28px;
        right: 12px;
        bottom: 50%;
        height: 1px;
    }

    .policy-point {
        position: absolute;
        left: var(--point-x);
        top: var(--point-y);
        width: 18px;
        height: 18px;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        background: var(--red);
        border: 3px solid #ffffff;
        box-shadow: 0 0 0 8px rgba(255,47,69,0.14), 0 0 28px rgba(255,47,69,0.75);
        z-index: 2;
    }

    .policy-label {
        position: absolute;
        color: var(--muted);
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        z-index: 1;
    }

    .policy-label.left { left: 12px; bottom: 49%; }
    .policy-label.right { right: 12px; bottom: 49%; color: var(--cyan); }
    .policy-label.bottom { left: 42%; bottom: 8px; }
    .policy-label.top { left: 42%; top: 10px; color: var(--yellow); }

    .policy-readout {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
        margin-top: 12px;
    }

    .policy-readout-item {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 10px 12px;
    }

    .policy-readout-label {
        color: var(--muted);
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .policy-readout-value {
        color: var(--text);
        font-size: 1rem;
        font-weight: 900;
        margin-top: 4px;
    }

    .strategy-list {
        display: grid;
        gap: 10px;
    }

    .strategy-row {
        display: grid;
        grid-template-columns: 38px 1fr auto;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .strategy-row:last-child {
        border-bottom: 0;
    }

    .lap {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        color: #0b1018;
        background: var(--yellow);
        font-weight: 900;
        font-size: 0.74rem;
    }

    .row-title {
        color: var(--text);
        font-weight: 800;
        font-size: 0.9rem;
    }

    .row-note {
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 2px;
    }

    .row-score {
        color: var(--cyan);
        font-weight: 900;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(23,31,45,0.96), rgba(13,18,27,0.96));
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 16px 18px;
    }

    [data-testid="stMetricLabel"] { color: var(--muted) !important; }
    [data-testid="stMetricValue"] { color: var(--text) !important; }

    .stSlider label {
        color: #d8e3ef !important;
        font-weight: 800;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 10px;
        overflow: hidden;
    }

    .footer {
        color: #697587;
        font-size: 0.75rem;
        text-align: center;
        padding-top: 22px;
        margin-top: 22px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    @media (max-width: 760px) {
        .race-strip {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .race-hero {
            padding: 22px 18px;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


# MODEL - Train
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
y_train = np.array([50, 80, 110, 90, 150])
model = LinearRegression().fit(X_train, y_train)

baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]


def run_simulation(new_iklan, new_diskon):
    pred = model.predict(np.array([[new_iklan, new_diskon]]))[0]
    delta_y = pred - baseline_pred
    return pred, delta_y


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def delta_status(value):
    if value > 5:
        return "Sangat Baik", "#25d366"
    if value > 0:
        return "Positif", "#f7c843"
    if value == 0:
        return "Netral", "#9aa8b8"
    return "Perlu Evaluasi", "#ff2f45"


def apply_chart_theme(fig, height=320):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=24, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#d8e3ef", family="Arial"),
        hovermode="x unified",
        showlegend=False,
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(color="#9aa8b8"),
        title_font=dict(color="#9aa8b8"),
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(color="#9aa8b8"),
        title_font=dict(color="#9aa8b8"),
    )
    return fig


# SIDEBAR
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 18px 0 12px 0;">
            <div style="font-size:2.8rem; font-weight:900; color:#ff2f45; line-height:1;">SIM</div>
            <div style="color:#f2f6fb; font-weight:900; font-size:1rem; margin-top:6px;">FRIKA ALDITIYO</div>
            <div style="color:#9aa8b8; font-size:0.75rem;">Dashboard Simulasi Kebijakan</div>
        </div>
        <hr style="border-color:#2a3547; margin: 8px 0 18px 0;">
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Pengaturan Simulasi")
    iklan_slider = st.slider("Anggaran Iklan (Juta Rp)", 0, 50, 10)
    diskon_slider = st.slider("Besaran Diskon (%)", 0, 50, 10)

    st.markdown("<hr style='border-color:#2a3547;'>", unsafe_allow_html=True)
    st.caption("Baseline: iklan Rp 10 Jt dan diskon 10%.")
    st.caption("Gunakan slider untuk melihat dampak perubahan kebijakan.")


# ENGINE
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)
status_label, status_color = delta_status(delta)

koef_iklan = abs(model.coef_[0])
koef_diskon = abs(model.coef_[1])
variabel_dominan = "Anggaran Iklan" if koef_iklan > koef_diskon else "Besaran Diskon"

performance_score = clamp(((hasil_pred - 30) / 130) * 100, 0, 100)
delta_score = clamp(((delta + 35) / 70) * 100, 0, 100)
policy_x = clamp(12 + (iklan_slider / 50) * 78, 10, 92)
policy_y = clamp(88 - (diskon_slider / 50) * 76, 10, 90)


st.markdown(
    """
<div class="race-hero">
    <span class="status-badge">Policy Simulator</span>
    <h1>Kebijakan Keuntungan Toko</h1>
    <p>Dashboard what-if untuk membaca dampak anggaran iklan dan diskon terhadap prediksi keuntungan dengan tampilan modern dan kontras.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="race-strip">
    <div class="race-tile">
        <div class="tile-label">Nama</div>
        <div class="tile-value">Frika</div>
        <div class="tile-sub">NPM 2313020008</div>
    </div>
    <div class="race-tile">
        <div class="tile-label">Status Skenario</div>
        <div class="tile-value" style="color:{status_color};">{status_label}</div>
        <div class="tile-sub">Berdasarkan delta profit</div>
    </div>
    <div class="race-tile">
        <div class="tile-label">Variabel Dominan</div>
        <div class="tile-value">{variabel_dominan}</div>
        <div class="tile-sub">Koefisien terbesar</div>
    </div>
    <div class="race-tile">
        <div class="tile-label">Indeks Hasil</div>
        <div class="tile-value">{performance_score:.0f}/100</div>
        <div class="tile-sub">Indeks visual skenario</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# METRIK
col1, col2, col3 = st.columns(3)
col1.metric("Baseline Keuntungan", f"Rp {baseline_pred:.2f} Jt")
col2.metric("Prediksi Intervensi", f"Rp {hasil_pred:.2f} Jt")
col3.metric("Delta Profit", f"Rp {delta:.2f} Jt", delta=f"{delta:.2f} Jt")


gauge_col, track_col = st.columns([1.15, 1])

with gauge_col:
    st.markdown(
        f"""
        <div class="gauge-card">
            <div class="card-title">Ringkasan Kinerja</div>
            <div style="display:flex; justify-content:space-between; gap:12px; color:#f2f6fb; font-weight:900; margin-bottom:8px;">
                <span>Potensi Profit</span><span>{performance_score:.1f}%</span>
            </div>
            <div class="speedbar"><div class="speedbar-fill" style="width:{performance_score:.1f}%;"></div></div>
            <div style="display:flex; justify-content:space-between; gap:12px; color:#f2f6fb; font-weight:900; margin:18px 0 8px 0;">
                <span>Skor Delta</span><span>{delta_score:.1f}%</span>
            </div>
            <div class="speedbar"><div class="speedbar-fill" style="width:{delta_score:.1f}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if delta > 0:
        st.success(
            f"Keputusan baik. Skenario ini meningkatkan keuntungan sebesar Rp {delta:.2f} Juta dibanding baseline."
        )
    elif delta < 0:
        st.error(
            f"Perhatian. Skenario ini menurunkan keuntungan sebesar Rp {abs(delta):.2f} Juta. Pertimbangkan ulang kebijakan ini."
        )
    else:
        st.info("Skenario ini menghasilkan keuntungan yang sama dengan baseline.")

with track_col:
    st.markdown(
        f"""
        <div class="gauge-card">
            <div class="card-title">Profil Kebijakan</div>
            <div class="policy-map" style="--point-x:{policy_x:.1f}%; --point-y:{policy_y:.1f}%;">
                <div class="policy-label left">Iklan rendah</div>
                <div class="policy-label right">Iklan tinggi</div>
                <div class="policy-label bottom">Diskon rendah</div>
                <div class="policy-label top">Diskon tinggi</div>
                <div class="policy-point"></div>
            </div>
            <div class="policy-readout">
                <div class="policy-readout-item">
                    <div class="policy-readout-label">Iklan</div>
                    <div class="policy-readout-value">Rp {iklan_slider} Jt</div>
                </div>
                <div class="policy-readout-item">
                    <div class="policy-readout-label">Diskon</div>
                    <div class="policy-readout-value">{diskon_slider}%</div>
                </div>
            </div>
            <div style="color:#9aa8b8; font-size:0.76rem; margin-top:10px;">
                Titik merah menunjukkan kombinasi kebijakan aktif.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# VISUALISASI
col_chart, col_tabel = st.columns([3, 2])

with col_chart:
    st.markdown("#### Perbandingan Skenario")
    data_plot = pd.DataFrame(
        {
            "Skenario": ["Baseline", "Intervensi"],
            "Keuntungan (Juta)": [round(baseline_pred, 2), round(hasil_pred, 2)],
        }
    )
    comparison_fig = go.Figure()
    comparison_fig.add_trace(
        go.Scatter(
            x=data_plot["Skenario"],
            y=data_plot["Keuntungan (Juta)"],
            mode="lines+markers+text",
            line=dict(color="#38d5ff", width=4, shape="spline", smoothing=1.2),
            marker=dict(
                size=18,
                color=["#9aa8b8", status_color],
                line=dict(color="#f2f6fb", width=2),
            ),
            fill="tozeroy",
            fillcolor="rgba(56, 213, 255, 0.16)",
            text=[f"Rp {value:.2f} Jt" for value in data_plot["Keuntungan (Juta)"]],
            textposition="top center",
            hovertemplate="%{x}<br>Keuntungan: Rp %{y:.2f} Jt<extra></extra>",
        )
    )
    comparison_fig = apply_chart_theme(comparison_fig, height=320)
    comparison_fig.update_yaxes(title_text="Keuntungan (Juta)")
    st.plotly_chart(comparison_fig, use_container_width=True)

with col_tabel:
    st.markdown("#### Ringkasan Input")
    df_summary = pd.DataFrame(
        {
            "Variabel": ["Anggaran Iklan", "Besaran Diskon"],
            "Baseline": ["Rp 10 Jt", "10%"],
            "Intervensi": [f"Rp {iklan_slider} Jt", f"{diskon_slider}%"],
            "Selisih": [f"{iklan_slider - 10:+} Jt", f"{diskon_slider - 10:+}%"],
        }
    )
    st.dataframe(df_summary, hide_index=True, use_container_width=True)

    st.markdown(
        f"""
        <div class="result-card">
            <div class="card-title">Info Model</div>
            <div style="color:#d8e3ef; font-size:0.88rem; line-height:1.7;">
                Algoritma: <b>Linear Regression</b><br>
                Fitur: Iklan, Diskon<br>
                Koefisien Iklan: <b>{model.coef_[0]:.4f}</b><br>
                Koefisien Diskon: <b>{model.coef_[1]:.4f}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# SENSITIVITY SWEEP
st.markdown("#### Analisis Sensitivitas")

col_s1, col_s2 = st.columns(2)

with col_s1:
    sweep_iklan = np.linspace(0, 50, 101)
    pred_iklan = [model.predict(np.array([[i, diskon_slider]]))[0] for i in sweep_iklan]
    df_iklan = pd.DataFrame(
        {"Anggaran Iklan (Juta)": sweep_iklan, "Prediksi Keuntungan": pred_iklan}
    )
    st.caption("Efek perubahan iklan saat diskon tetap.")
    iklan_fig = go.Figure()
    iklan_fig.add_trace(
        go.Scatter(
            x=df_iklan["Anggaran Iklan (Juta)"],
            y=df_iklan["Prediksi Keuntungan"],
            mode="lines",
            line=dict(color="#ff2f45", width=4, shape="spline", smoothing=1.25),
            fill="tozeroy",
            fillcolor="rgba(255, 47, 69, 0.14)",
            hovertemplate="Iklan: Rp %{x:.1f} Jt<br>Prediksi: Rp %{y:.2f} Jt<extra></extra>",
        )
    )
    iklan_fig.add_trace(
        go.Scatter(
            x=[iklan_slider],
            y=[hasil_pred],
            mode="markers",
            marker=dict(size=16, color="#f7c843", line=dict(color="#f2f6fb", width=2)),
            hovertemplate="Skenario aktif<br>Rp %{x:.1f} Jt<br>Rp %{y:.2f} Jt<extra></extra>",
        )
    )
    iklan_fig = apply_chart_theme(iklan_fig, height=250)
    iklan_fig.update_xaxes(title_text="Anggaran Iklan (Juta)")
    iklan_fig.update_yaxes(title_text="Prediksi Keuntungan")
    st.plotly_chart(iklan_fig, use_container_width=True)

with col_s2:
    sweep_diskon = np.linspace(0, 50, 101)
    pred_diskon = [model.predict(np.array([[iklan_slider, d]]))[0] for d in sweep_diskon]
    df_diskon = pd.DataFrame(
        {"Besaran Diskon (%)": sweep_diskon, "Prediksi Keuntungan": pred_diskon}
    )
    st.caption("Efek perubahan diskon saat iklan tetap.")
    diskon_fig = go.Figure()
    diskon_fig.add_trace(
        go.Scatter(
            x=df_diskon["Besaran Diskon (%)"],
            y=df_diskon["Prediksi Keuntungan"],
            mode="lines",
            line=dict(color="#25d366", width=4, shape="spline", smoothing=1.25),
            fill="tozeroy",
            fillcolor="rgba(37, 211, 102, 0.14)",
            hovertemplate="Diskon: %{x:.1f}%<br>Prediksi: Rp %{y:.2f} Jt<extra></extra>",
        )
    )
    diskon_fig.add_trace(
        go.Scatter(
            x=[diskon_slider],
            y=[hasil_pred],
            mode="markers",
            marker=dict(size=16, color="#f7c843", line=dict(color="#f2f6fb", width=2)),
            hovertemplate="Skenario aktif<br>%{x:.1f}%<br>Rp %{y:.2f} Jt<extra></extra>",
        )
    )
    diskon_fig = apply_chart_theme(diskon_fig, height=250)
    diskon_fig.update_xaxes(title_text="Besaran Diskon (%)")
    diskon_fig.update_yaxes(title_text="Prediksi Keuntungan")
    st.plotly_chart(diskon_fig, use_container_width=True)


# FEATURE TAMBAHAN: PERBANDINGAN SKENARIO
st.markdown("#### Perbandingan Alternatif Skenario")
scenario_grid = []
for iklan_candidate, diskon_candidate, label in [
    (10, 10, "Baseline"),
    (20, 10, "Naikkan iklan"),
    (10, 20, "Naikkan diskon"),
    (25, 15, "Kombinasi seimbang"),
    (35, 8, "Iklan agresif"),
]:
    pred_candidate, delta_candidate = run_simulation(iklan_candidate, diskon_candidate)
    scenario_grid.append(
        {
            "Setup": label,
            "Iklan": iklan_candidate,
            "Diskon": diskon_candidate,
            "Prediksi": pred_candidate,
            "Delta": delta_candidate,
        }
    )

df_scout = pd.DataFrame(scenario_grid).sort_values("Prediksi", ascending=False)

scout_col, plan_col = st.columns([1, 1])

with scout_col:
    st.dataframe(
        df_scout.assign(
            Prediksi=df_scout["Prediksi"].map(lambda value: f"Rp {value:.2f} Jt"),
            Delta=df_scout["Delta"].map(lambda value: f"{value:+.2f} Jt"),
        ),
        hide_index=True,
        use_container_width=True,
    )

with plan_col:
    best_setup = df_scout.iloc[0]
    st.markdown(
        f"""
        <div class="strategy-card">
            <div class="card-title">Ringkasan Rekomendasi</div>
            <div class="strategy-list">
                <div class="strategy-row">
                    <div class="lap">1</div>
                    <div>
                        <div class="row-title">Skenario saat ini</div>
                        <div class="row-note">Iklan Rp {iklan_slider} Jt, diskon {diskon_slider}%</div>
                    </div>
                    <div class="row-score">Rp {hasil_pred:.1f}</div>
                </div>
                <div class="strategy-row">
                    <div class="lap">2</div>
                    <div>
                        <div class="row-title">Alternatif terbaik</div>
                        <div class="row-note">{best_setup["Setup"]}: iklan Rp {best_setup["Iklan"]} Jt, diskon {best_setup["Diskon"]}%</div>
                    </div>
                    <div class="row-score">Rp {best_setup["Prediksi"]:.1f}</div>
                </div>
                <div class="strategy-row">
                    <div class="lap">3</div>
                    <div>
                        <div class="row-title">Fokus evaluasi</div>
                        <div class="row-note">Variabel paling sensitif dari model</div>
                    </div>
                    <div class="row-score">{variabel_dominan}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# KESIMPULAN WHAT-IF
st.markdown("---")
st.markdown("#### Kesimpulan Analisis What-If")

if delta > 5:
    status = "sangat menguntungkan"
    rekomendasi = "Skenario ini <b>layak diterapkan</b>. Pertahankan kombinasi kebijakan ini."
elif delta > 0:
    status = "sedikit menguntungkan"
    rekomendasi = "Skenario ini memberikan hasil positif namun <b>belum signifikan</b>. Coba naikkan anggaran iklan lebih lanjut."
elif delta == 0:
    status = "netral"
    rekomendasi = "Tidak ada perubahan berarti. <b>Coba ubah salah satu variabel</b> untuk melihat dampaknya."
elif delta > -5:
    status = "sedikit merugikan"
    rekomendasi = "Skenario ini <b>kurang disarankan</b>. Pertimbangkan untuk mengurangi besaran diskon."
else:
    status = "sangat merugikan"
    rekomendasi = "Skenario ini <b>tidak disarankan</b>. Kembali ke kondisi baseline atau cari kombinasi lain."

st.markdown(
    f"""
<div style="background:linear-gradient(180deg, rgba(23,31,45,0.96), rgba(13,18,27,0.96)); border:1px solid #2a3547; border-left: 5px solid {status_color};
            border-radius:10px; padding:20px 24px; margin-top:8px;">
    <p style="color:#9aa8b8; font-size:0.78rem; font-weight:900; margin:0 0 10px 0; text-transform:uppercase;">Hasil Simulasi What-If</p>
    <p style="color:#f2f6fb; margin:0 0 8px 0;">
        Dengan <b style="color:#38d5ff;">Iklan = Rp {iklan_slider} Juta</b> dan
        <b style="color:#38d5ff;">Diskon = {diskon_slider}%</b>,
        skenario ini dinilai <b style="color:#f7c843;">{status}</b>
        dengan perubahan keuntungan sebesar
        <b style="color:{status_color};">Rp {delta:.2f} Juta</b>
        dari kondisi baseline.
    </p>
    <p style="color:#f2f6fb; margin:0 0 8px 0;">
        Variabel paling sensitif adalah
        <b style="color:#38d5ff;">{variabel_dominan}</b>
        dengan koefisien <b style="color:#38d5ff;">{max(koef_iklan, koef_diskon):.4f}</b>.
    </p>
    <p style="color:#d8e3ef; margin:0;"><b>Rekomendasi:</b> {rekomendasi}</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        Frika Alditiyo - Praktikum Pemodelan & Simulasi Minggu 14
    </div>
    """,
    unsafe_allow_html=True,
)
