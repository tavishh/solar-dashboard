import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Solar Data Optimisation Analytics Dashboard",
    page_icon="",
    layout="wide",
)

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stSidebar"] {
    background-color: #f8f9fb;
    border-right: 1px solid #e4e7ec;
}

[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e4e7ec;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem;
    font-weight: 600;
    color: #8a94a6;
    text-transform: uppercase;
    letter-spacing: 1px;
}
    color: #111827;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace;
    font-size: 1.65rem;
    font-weight: 500;
}
.page-title {
    font-size: 2.8rem !important;
    font-weight: 600;
    color: #111827;
    margin-bottom: 2px;
    text-align: center;
}
.page-sub {
    font-size: 0.85rem;
    color: #6b7280;
    margin-bottom: 20px;
    text-align: center;
}
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 10px;
}
.insight-box {
    background: #f0f7ff;
    border-left: 3px solid #2563eb;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #1e3a5f;
    line-height: 1.6;
    margin-bottom: 16px;
}
.weight-chip {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px 3px;
}
.zero-chip {
    display: inline-block;
    background: #f3f4f6;
    color: #9ca3af;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px 3px;
}
hr { border: none; border-top: 1px solid #e4e7ec; margin: 24px 0; }
h3 { color: #111827; font-size: 1rem; font-weight: 600; }

/* Footer */
.footer {
    position: fixed;
    bottom: 0;
    left: 20px;
    right: 0;
    background: #ffffff;
    border-top: 1px solid #e4e7ec;
    padding: 10px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #9ca3af;
    z-index: 999;
}
.footer a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
}
.footer a:hover { text-decoration: underline; }

</style>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span><strong>Solar Data Optimisation Analytics Dashboard</strong> &nbsp;·&nbsp; Courtesy of the University of Mauritius and Dr. Yatindra Ramgolam</span>
    <span>
        Created by <strong>Tavish Hookoom</strong>
        &nbsp;·&nbsp;
        <a href="https://github.com/tavishh" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                 fill="currentColor" style="vertical-align:middle; margin-right:3px; color:#2563eb">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57
                       0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41
                       -1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815
                       2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925
                       0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23
                       .96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65
                       .24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925
                       .435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57
                       A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
            </svg>
            github.com/tavishh
        </a>
        &nbsp;·&nbsp; Built with Python · Streamlit · Plotly
    </span>
</div>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
SITE_NAMES = [
    "Curepipe", "La Mivoie", "Ferney", "Mahebourg",
    "Souillac", "Goodlands", "Rose Hill", "Nicolay", "Bramsthan"
]
IRR_COLS = list(range(2, 11))   # cols 2–10: raw irradiance per site
PWR_COLS = list(range(17, 26))  # cols 17–25: GRG-weighted power per site
COMBINED_COL  = 26   # Normalised Total Power (GRG optimised combined output)
ABS_DIFF_COL  = 28   # Absolute minute-to-minute ramp rate of combined output

SITE_COLORS = [
    "#2563eb", "#dc2626", "#16a34a", "#d97706",
    "#7c3aed", "#0891b2", "#db2777", "#65a30d", "#9333ea"
]

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data...")
def load_data(source):
    xl = pd.ExcelFile(source)
    day_sheets = [s for s in xl.sheet_names if s != "Summary" and len(s.split()) == 2 and s.split()[1].isdigit()]

    frames = []
    for sheet in day_sheets:
        month_abbr = sheet.split()[0]   # e.g. "Jan", "Mar"
        day_num    = int(sheet.split()[1])
        # Find the year from the Summary sheet date if possible, default 2020
        date = pd.to_datetime(f"{month_abbr} {day_num} 2020", format="%b %d %Y")
        df_raw   = pd.read_excel(source, sheet_name=sheet, header=None)

        # GRG weights are stored in row 2 (index 2), cols 17–25
        grg_weights = [
            float(v) if pd.notna(v) else 0.0
            for v in df_raw.iloc[2, 17:26].tolist()
        ]

        # Data starts at row 4 (index 4)
        df = df_raw.iloc[4:].copy().reset_index(drop=True)

        # Parse time column
        times  = pd.to_datetime(df[0].astype(str), format="%H:%M:%S", errors="coerce")
        valid  = times.notna()
        df     = df[valid].reset_index(drop=True)
        times  = times[valid].reset_index(drop=True)

        datetimes = [pd.Timestamp.combine(date.date(), t.time()) for t in times]
        out = pd.DataFrame({"datetime": datetimes})

        # Raw irradiance (W/m²) per site
        for i, (name, col) in enumerate(zip(SITE_NAMES, IRR_COLS)):
            out[f"irr_{name}"] = pd.to_numeric(df[col], errors="coerce")

        # Normalised power per site (GRG-weighted contribution)
        for name, col in zip(SITE_NAMES, PWR_COLS):
            out[f"pwr_{name}"] = pd.to_numeric(df[col], errors="coerce")

        # GRG optimised combined output (col 26)
        out["grg_combined"] = pd.to_numeric(df[COMBINED_COL], errors="coerce")

        # Ramp rate of combined output (col 28)
        out["ramp_rate"] = pd.to_numeric(df[ABS_DIFF_COL], errors="coerce")

        # Store weights (same for every row on that day)
        for name, w in zip(SITE_NAMES, grg_weights):
            out[f"w_{name}"] = w

        frames.append(out)

    return pd.concat(frames, ignore_index=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Solar Data Dashboard")
    st.divider()

    BUNDLED = os.path.join(os.path.dirname(__file__), "data", "01_January.xlsx")
    uploaded = st.file_uploader("Upload data file (.xlsx)", type=["xlsx"])

    if uploaded:
        source = uploaded
        st.success("File uploaded")
    elif os.path.exists(BUNDLED):
        source = BUNDLED
        st.info("Using bundled dataset")
    else:
        source = None
        st.warning("Upload your data file (.xlsx) to begin")

    if source:
        df = load_data(source)

        st.divider()
        st.markdown("**Select a day**")
        all_dates = sorted(df["datetime"].dt.date.unique())
        selected_date = st.selectbox(
            "Day",
            all_dates,
            format_func=lambda d: d.strftime("%B %d, %Y"),
        )

        st.divider()
        st.markdown("**Reference site**")
        st.markdown("<small>Used as the 'before' in the before/after comparison</small>", unsafe_allow_html=True)
        ref_site = st.selectbox("Single site baseline", SITE_NAMES, index=4)  # default Souillac (highest weight)

if not source:
    st.markdown('<p class="page-title">Solar PV Dashboard · Mauritius</p>', unsafe_allow_html=True)
    st.info("👈 Upload your data file in the sidebar to get started.")
    st.stop()

# ── Filter to selected day ─────────────────────────────────────────────────────
df_day = df[df["datetime"].dt.date == selected_date].sort_values("datetime").reset_index(drop=True)
times  = df_day["datetime"]

# GRG weights for this day (read from first row)
weights = {name: df_day[f"w_{name}"].iloc[0] for name in SITE_NAMES}
active_sites = [name for name, w in weights.items() if w > 0]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="page-title">Solar Data Optimisation Analytics Dashboard</p>', unsafe_allow_html=True)
month_label = df["datetime"].dt.strftime("%B %Y").iloc[0]

st.markdown(
    f'<p class="page-sub">University of Mauritius · {month_label} · '
    '9 sites · 1-minute resolution · GRG geographic dispersion optimisation</p>',
    unsafe_allow_html=True
)
st.divider()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡  Before vs After Optimisation",
    "🌤  Irradiance by Site",
    "📅  Monthly Overview",
    "🔬  Research & Pipeline",
])


# ════════════════════════════
# TAB 1 - Before vs After
# ════════════════════════════
with tab1:

    # Insight box
    st.markdown(f"""
    <div class="insight-box">
        <strong>What you're seeing:</strong> The GRG (Generalised Reduced Gradient) solver allocated
        optimal percentage weights to each of the 9 PV sites so that their combined output is as smooth
        as possible. Rather than relying on a single site, which fluctuates sharply when clouds pass,
        the optimised combined signal averages out local cloud events across geographically separated
        locations, reducing grid intermittency by up to <strong>67%</strong>.
        The <span style="color:#2563eb;font-weight:600">blue line</span> is the GRG-optimised output.
        The <span style="color:#e5383b;font-weight:600">red line</span> is a single site alone.
    </div>
    """, unsafe_allow_html=True)

    # GRG weights display
    st.markdown('<p class="section-label">GRG Solver Weights: ' + selected_date.strftime("%B %d, %Y") + '</p>', unsafe_allow_html=True)
    chips_html = ""
    for name in SITE_NAMES:
        w = weights[name]
        if w > 0:
            chips_html += f'<span class="weight-chip">{name} {w:.1f}%</span>'
        else:
            chips_html += f'<span class="zero-chip">{name} 0%</span>'
    st.markdown(chips_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main before/after chart ────────────────────────────────────────────────
    single_irr  = df_day[f"irr_{ref_site}"].fillna(0) / 1000   # normalise to 0–1
    grg_out     = df_day["grg_combined"].fillna(0)

    fig_ba = go.Figure()

    # Single site (before)
    fig_ba.add_trace(go.Scatter(
        x=times, y=single_irr,
        name=f"Single site: {ref_site}",
        mode="lines",
        line=dict(color="#e5383b", width=1.6),
        opacity=0.85,
        hovertemplate="%{x|%H:%M}<br>Power: %{y:.3f} p.u.<extra></extra>",
    ))

    # GRG combined (after)
    fig_ba.add_trace(go.Scatter(
        x=times, y=grg_out,
        name="GRG optimised (combined)",
        mode="lines",
        line=dict(color="#2563eb", width=2.2),
        hovertemplate="%{x|%H:%M}<br>GRG output: %{y:.3f} p.u.<extra></extra>",
    ))

    fig_ba.update_layout(
        paper_bgcolor="white", plot_bgcolor="#fafbfc",
        font=dict(family="DM Sans, sans-serif", size=12, color="#374151"),
        height=400,
        margin=dict(l=55, r=20, t=30, b=50),
        xaxis=dict(title="Time of Day", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
        yaxis=dict(title="Normalised Power Output (p.u.)", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
        legend=dict(bgcolor="white", bordercolor="#e4e7ec", borderwidth=1,
                    font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, x=0),
        hovermode="x unified",
    )
    st.plotly_chart(fig_ba, use_container_width=True)

    # ── Ramp rate comparison ───────────────────────────────────────────────────
    st.markdown('<p class="section-label">Ramp Rate: Minute-to-Minute Output Change</p>', unsafe_allow_html=True)

    single_ramp = single_irr.diff().abs().fillna(0)
    grg_ramp    = df_day["ramp_rate"].fillna(0)

    fig_ramp = go.Figure()
    fig_ramp.add_trace(go.Scatter(
        x=times, y=single_ramp,
        name=f"Single site: {ref_site}",
        mode="lines",
        line=dict(color="#e5383b", width=1.4),
        opacity=0.8,
        fill="tozeroy", fillcolor="rgba(229,56,59,0.07)",
        hovertemplate="%{x|%H:%M}<br>Ramp: %{y:.4f} p.u./min<extra></extra>",
    ))
    fig_ramp.add_trace(go.Scatter(
        x=times, y=grg_ramp,
        name="GRG optimised",
        mode="lines",
        line=dict(color="#2563eb", width=1.4),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
        hovertemplate="%{x|%H:%M}<br>Ramp: %{y:.4f} p.u./min<extra></extra>",
    ))
    fig_ramp.update_layout(
        paper_bgcolor="white", plot_bgcolor="#fafbfc",
        font=dict(family="DM Sans, sans-serif", size=12, color="#374151"),
        height=260,
        margin=dict(l=55, r=20, t=20, b=50),
        xaxis=dict(title="Time of Day", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
        yaxis=dict(title="|ΔP| per minute (p.u.)", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
        legend=dict(bgcolor="white", bordercolor="#e4e7ec", borderwidth=1,
                    font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, x=0),
        hovermode="x unified",
    )
    st.plotly_chart(fig_ramp, use_container_width=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    st.divider()
    st.markdown('<p class="section-label">Day Summary - ' + selected_date.strftime("%B %d, %Y") + '</p>', unsafe_allow_html=True)

    single_mean_ramp = single_ramp[single_ramp > 0].mean()
    grg_mean_ramp    = grg_ramp[grg_ramp > 0].mean()
    ramp_reduction   = (1 - grg_mean_ramp / single_mean_ramp) * 100 if single_mean_ramp > 0 else 0

    thresh = 0.05
    single_events = int((single_ramp > thresh).sum())
    grg_events    = int((grg_ramp > thresh).sum())
    event_reduction = (1 - grg_events / single_events) * 100 if single_events > 0 else 0

    peak_grg    = grg_out.max()
    n_active    = len(active_sites)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean Ramp Reduction",   f"{ramp_reduction:.1f}%",    "GRG vs single site")
    c2.metric("Grid Events (single)",  f"{single_events}",          f">{thresh} p.u./min")
    c3.metric("Grid Events (GRG)",     f"{grg_events}",             f"↓ {event_reduction:.0f}%")
    c4.metric("Active Sites (GRG)",    f"{n_active}",               "Sites with weight > 0")


# ════════════════════════════
# TAB 2 - Irradiance by Site
# ════════════════════════════
with tab2:
    st.markdown('<p class="section-label">Raw irradiance per site - ' + selected_date.strftime("%B %d, %Y") + '</p>', unsafe_allow_html=True)

    selected_sites = st.multiselect(
        "Choose sites to display",
        SITE_NAMES,
        default=SITE_NAMES,
        key="irr_sites",
    )

    if selected_sites:
        fig_irr = go.Figure()
        for i, name in enumerate(selected_sites):
            color = SITE_COLORS[SITE_NAMES.index(name)]
            y = df_day[f"irr_{name}"]
            fig_irr.add_trace(go.Scatter(
                x=times, y=y,
                name=name,
                mode="lines",
                line=dict(color=color, width=1.6),
                hovertemplate=f"{name}<br>%{{x|%H:%M}}<br>%{{y:.0f}} W/m²<extra></extra>",
            ))

        fig_irr.update_layout(
            paper_bgcolor="white", plot_bgcolor="#fafbfc",
            font=dict(family="DM Sans, sans-serif", size=12, color="#374151"),
            height=420,
            margin=dict(l=55, r=20, t=30, b=50),
            xaxis=dict(title="Time of Day", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
            yaxis=dict(title="Irradiance (W/m²)", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
            legend=dict(bgcolor="white", bordercolor="#e4e7ec", borderwidth=1,
                        font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, x=0),
            hovermode="x unified",
        )
        st.plotly_chart(fig_irr, use_container_width=True)

        # Daily stats table
        st.divider()
        st.markdown('<p class="section-label">Daily Statistics</p>', unsafe_allow_html=True)
        stats_rows = []
        for name in selected_sites:
            irr = df_day[f"irr_{name}"].dropna()
            stats_rows.append({
                "Site": name,
                "Peak (W/m²)": f"{irr.max():.0f}" if len(irr) else "-",
                "Mean (W/m²)": f"{irr.mean():.0f}" if len(irr) else "-",
                "GRG Weight": f"{weights[name]:.1f}%" if weights[name] > 0 else "Not selected",
            })
        st.dataframe(pd.DataFrame(stats_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Select at least one site above.")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 - Monthly Overview
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f'<p class="section-label">Monthly summary - {month_label}</p>', unsafe_allow_html=True)

    # Daily peak irradiance per site
    daily_peaks = (
        df.groupby(df["datetime"].dt.date)[[f"irr_{n}" for n in SITE_NAMES]]
        .max()
        .reset_index()
    )
    daily_peaks.columns = ["date"] + SITE_NAMES

    # Daily mean ramp rate of GRG combined
    daily_ramp = (
        df.groupby(df["datetime"].dt.date)["ramp_rate"]
        .mean()
        .reset_index()
    )
    daily_ramp.columns = ["date", "mean_ramp"]

    # Daily peak GRG combined output
    daily_grg = (
        df.groupby(df["datetime"].dt.date)["grg_combined"]
        .max()
        .reset_index()
    )
    daily_grg.columns = ["date", "peak_grg"]

    # ── Monthly KPIs ──────────────────────────────────────────────────────────
    best_day  = daily_grg.loc[daily_grg["peak_grg"].idxmax(), "date"].strftime("%b %d")
    avg_ramp  = daily_ramp["mean_ramp"].mean()
    best_site = max(SITE_NAMES, key=lambda n: daily_peaks[n].mean())

    c1, c2, c3 = st.columns(3)
    c1.metric("Best Output Day",      best_day,              "Highest peak GRG output")
    c2.metric("Avg Daily Ramp Rate",  f"{avg_ramp:.4f} p.u.", "Combined GRG output")
    c3.metric("Highest Avg Irradiance Site", best_site,      "Across all 31 days")

    st.divider()

    # ── Monthly irradiance heatmap ─────────────────────────────────────────────
    st.markdown('<p class="section-label">Daily Peak Irradiance by Site (W/m²)</p>', unsafe_allow_html=True)

    z_vals = daily_peaks[SITE_NAMES].values.T
    x_dates = [str(d) for d in daily_peaks["date"]]

    fig_hm = go.Figure(data=go.Heatmap(
        z=z_vals,
        x=x_dates,
        y=SITE_NAMES,
        colorscale="YlOrRd",
        hovertemplate="Site: %{y}<br>Date: %{x}<br>Peak: %{z:.0f} W/m²<extra></extra>",
        colorbar=dict(title="W/m²", thickness=14),
    ))
    fig_hm.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans, sans-serif", size=11, color="#374151"),
        height=340,
        margin=dict(l=100, r=20, t=20, b=60),
        xaxis=dict(title="", tickangle=-45, showgrid=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    # ── GRG ramp rate trend across the month ──────────────────────────────────
    st.markdown('<p class="section-label">Daily Mean Ramp Rate - GRG Optimised Output</p>', unsafe_allow_html=True)

    fig_rtrend = go.Figure()
    fig_rtrend.add_trace(go.Bar(
        x=[str(d) for d in daily_ramp["date"]],
        y=daily_ramp["mean_ramp"],
        marker_color="#2563eb",
        opacity=0.75,
        hovertemplate="%{x}<br>Mean ramp: %{y:.5f} p.u./min<extra></extra>",
    ))
    fig_rtrend.update_layout(
        paper_bgcolor="white", plot_bgcolor="#fafbfc",
        font=dict(family="DM Sans, sans-serif", size=12, color="#374151"),
        height=260,
        margin=dict(l=60, r=20, t=10, b=60),
        xaxis=dict(title="", tickangle=-45, showgrid=False),
        yaxis=dict(title="Mean ramp rate (p.u./min)", showgrid=True, gridcolor="#f0f2f5", zeroline=False),
        showlegend=False,
    )
    st.plotly_chart(fig_rtrend, use_container_width=True)
    st.caption(
        "Lower ramp rate = smoother output = less stress on the grid. "
        "The GRG optimisation minimises this value by finding the ideal geographic weighting."
    )


# ════════════════════════════════════════════
# TAB 4 - Research Pipeline & Publications
# ════════════════════════════════════════════
with tab4:

    # ── Pipeline header ───────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Data Processing Pipeline</p>', unsafe_allow_html=True)
    st.markdown("### From Raw Sensor Data to Optimised Grid Output")
    st.markdown(
        "<p style='color:#6b7280; font-size:0.88rem; margin-bottom:20px'>"
        "10 sites &nbsp;·&nbsp; 12 months &nbsp;·&nbsp; 306,600 readings/site "
        "&nbsp;·&nbsp; BSRN quality-controlled &nbsp;·&nbsp; GRG optimised"
        "</p>",
        unsafe_allow_html=True,
    )

    # ── Generate illustrative signals ─────────────────────────────────────────
    rng = np.random.default_rng(42)
    n = 120
    t = np.linspace(0, np.pi, n)

    def make_raw(seed):
        r = np.random.default_rng(seed)
        bell = np.sin(np.linspace(0, np.pi, n)) * 0.85
        noise = (r.random(n) - 0.5) * 0.45
        spikes = np.where(r.random(n) > 0.93,
                          (r.random(n) - 0.5) * 0.9, 0)
        return np.clip(bell + noise + spikes, -0.15, 1.25)

    raw1 = make_raw(42)
    raw2 = make_raw(99)
    raw3 = make_raw(7)

    # QC flags
    upper_lim, lower_lim = 1.05, 0.0
    flagged_mask = (raw2 > upper_lim) | (raw2 < lower_lim)
    cleaned = np.clip(raw2, lower_lim, upper_lim)

    # Smoothed combined
    window = 9
    kernel = np.ones(window) / window
    combined_smooth = np.convolve(raw3, kernel, mode="same")
    times_x = list(range(n))

    # ── Stage 1 - Raw data ────────────────────────────────────────────────────
    c1, arr1, c2, arr2, c3 = st.columns([10, 1, 10, 1, 10])

    with c1:
        st.markdown("""
        <div style='border:1px solid #e4e7ec; border-radius:14px; padding:18px 20px;
                    background:white; box-shadow:0 1px 4px rgba(0,0,0,0.05);
                    border-top: 3px solid #2563eb; height:100%'>
          <div style='display:flex; align-items:center; gap:10px; margin-bottom:14px'>
            <div style='width:26px; height:26px; border-radius:50%; background:#dbeafe;
                        color:#2563eb; font-weight:700; font-size:12px;
                        display:flex; align-items:center; justify-content:center'>1</div>
            <div style='font-weight:600; font-size:13px; color:#111827'>Raw Ground & Satellite Data</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        fig_raw = go.Figure()
        fig_raw.add_trace(go.Scatter(
            x=times_x, y=raw1, mode="lines",
            line=dict(color="#2563eb", width=1.6),
            fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
            hoverinfo="skip",
        ))
        fig_raw.update_layout(
            paper_bgcolor="white", plot_bgcolor="#fafbfc",
            height=140, margin=dict(l=30, r=10, t=10, b=20),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0", zeroline=False,
                       title=dict(text="Irradiance", font=dict(size=10))),
            showlegend=False,
        )
        st.plotly_chart(fig_raw, use_container_width=True)
        st.markdown("""
        <div style='font-size:11px; color:#6b7280; line-height:1.6; margin-top:4px'>
          Raw 1-minute irradiance readings from ground-based sensors and satellite sources
          across 10 sites in Mauritius. Arrives as unvalidated CSV files per site per month.
        </div>
        <div style='margin-top:10px; padding:8px 11px; background:#dbeafe; border-radius:8px;
                    font-size:10.5px; color:#2563eb; font-weight:600; line-height:1.6'>
          25,000–30,000 readings/site/month · 1-min resolution · CSV format
        </div>
        """, unsafe_allow_html=True)

    with arr1:
        st.markdown("<div style='padding-top:80px; text-align:center; color:#9ca3af; font-size:22px'>→</div>",
                    unsafe_allow_html=True)

    # ── Stage 2 - Quality Control ─────────────────────────────────────────────
    with c2:
        st.markdown("""
        <div style='border:1px solid #e4e7ec; border-radius:14px; padding:18px 20px;
                    background:white; box-shadow:0 1px 4px rgba(0,0,0,0.05);
                    border-top: 3px solid #d97706; height:100%'>
          <div style='display:flex; align-items:center; gap:10px; margin-bottom:14px'>
            <div style='width:26px; height:26px; border-radius:50%; background:#fef3c7;
                        color:#d97706; font-weight:700; font-size:12px;
                        display:flex; align-items:center; justify-content:center'>2</div>
            <div style='font-weight:600; font-size:13px; color:#111827'>BSRN Quality Control</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        fig_qc = go.Figure()
        # BSRN limit lines
        fig_qc.add_hline(y=upper_lim, line_dash="dot", line_color="#d97706",
                          line_width=1.4, annotation_text="BSRN upper",
                          annotation_font=dict(size=9, color="#d97706"))
        fig_qc.add_hline(y=lower_lim, line_dash="dot", line_color="#d97706",
                          line_width=1.4, annotation_text="BSRN lower",
                          annotation_position="bottom right",
                          annotation_font=dict(size=9, color="#d97706"))
        # Cleaned signal
        fig_qc.add_trace(go.Scatter(
            x=times_x, y=cleaned, mode="lines",
            line=dict(color="#d97706", width=1.6),
            fill="tozeroy", fillcolor="rgba(217,119,6,0.07)",
            hoverinfo="skip",
        ))
        # Flagged points
        flagged_x = [i for i in range(n) if flagged_mask[i]]
        flagged_y = [raw2[i] for i in flagged_x]
        if flagged_x:
            fig_qc.add_trace(go.Scatter(
                x=flagged_x, y=flagged_y, mode="markers",
                marker=dict(color="#dc2626", size=6, symbol="x"),
                hoverinfo="skip", showlegend=False,
            ))
        fig_qc.update_layout(
            paper_bgcolor="white", plot_bgcolor="#fafbfc",
            height=140, margin=dict(l=30, r=10, t=10, b=20),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0", zeroline=False,
                       title=dict(text="Irradiance", font=dict(size=10))),
            showlegend=False,
        )
        st.plotly_chart(fig_qc, use_container_width=True)
        st.markdown(f"""
        <div style='font-size:11px; color:#6b7280; line-height:1.6; margin-top:4px'>
          Each reading tested against dynamic BSRN upper and lower irradiance limits.
          Out-of-range values (<span style='color:#dc2626; font-weight:600'>red ✕</span>)
          flagged and excluded, preserving 99.74% of obtained data.
        </div>
        <div style='margin-top:10px; padding:8px 11px; background:#fef3c7; border-radius:8px;
                    font-size:10.5px; color:#d97706; font-weight:600; line-height:1.6'>
          99.74% data passed QC · Flagged readings removed · BSRN international standard
        </div>
        """, unsafe_allow_html=True)

    with arr2:
        st.markdown("<div style='padding-top:80px; text-align:center; color:#9ca3af; font-size:22px'>→</div>",
                    unsafe_allow_html=True)

    # ── Stage 3 - GRG Optimisation ────────────────────────────────────────────
    with c3:
        st.markdown("""
        <div style='border:1px solid #e4e7ec; border-radius:14px; padding:18px 20px;
                    background:white; box-shadow:0 1px 4px rgba(0,0,0,0.05);
                    border-top: 3px solid #16a34a; height:100%'>
          <div style='display:flex; align-items:center; gap:10px; margin-bottom:14px'>
            <div style='width:26px; height:26px; border-radius:50%; background:#dcfce7;
                        color:#16a34a; font-weight:700; font-size:12px;
                        display:flex; align-items:center; justify-content:center'>3</div>
            <div style='font-weight:600; font-size:13px; color:#111827'>GRG Optimisation - Before vs After</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        fig_opt = go.Figure()
        fig_opt.add_trace(go.Scatter(
            x=times_x, y=raw3, name="Single site (before)",
            mode="lines", line=dict(color="#dc2626", width=1.4, dash="dot"),
            hoverinfo="skip",
        ))
        fig_opt.add_trace(go.Scatter(
            x=times_x, y=combined_smooth, name="GRG combined (after)",
            mode="lines", line=dict(color="#16a34a", width=2.0),
            fill="tozeroy", fillcolor="rgba(22,163,74,0.07)",
            hoverinfo="skip",
        ))
        fig_opt.update_layout(
            paper_bgcolor="white", plot_bgcolor="#fafbfc",
            height=140, margin=dict(l=30, r=10, t=10, b=20),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0", zeroline=False,
                       title=dict(text="Power (p.u.)", font=dict(size=10))),
            legend=dict(font=dict(size=9), bgcolor="white",
                        bordercolor="#e4e7ec", borderwidth=1,
                        x=0.01, y=0.99),
        )
        st.plotly_chart(fig_opt, use_container_width=True)
        st.markdown("""
        <div style='font-size:11px; color:#6b7280; line-height:1.6; margin-top:4px'>
          GRG solver assigns optimal weights per site. Geographic dispersion smooths
          cloud-induced fluctuations, delivering a stable combined output to the grid.
        </div>
        <div style='margin-top:10px; padding:8px 11px; background:#dcfce7; border-radius:8px;
                    font-size:10.5px; color:#16a34a; font-weight:600; line-height:1.6'>
          Up to 67% intermittency reduction · 9 active sites · Weights optimised per month
        </div>
        """, unsafe_allow_html=True)

    # ── Stat cards ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4, s5 = st.columns(5)
    for col, val, label, sub, color in [
        (s1, "10",     "Sites",                   "across Mauritius",        "#2563eb"),
        (s2, "3M+",    "Total Readings",           "per year, all sites",     "#2563eb"),
        (s3, "99.74%", "Data Quality",             "BSRN validated",          "#d97706"),
        (s4, "≤67%",   "Intermittency Reduction",  "GRG optimised output",    "#16a34a"),
        (s5, "5",      "Publications",             "peer-reviewed journals",  "#6b7280"),
    ]:
        col.markdown(f"""
        <div style='background:white; border:1px solid #e4e7ec; border-radius:12px;
                    padding:14px 16px; box-shadow:0 1px 3px rgba(0,0,0,0.04)'>
          <div style='font-size:22px; font-weight:700; color:{color};
                      font-variant-numeric:tabular-nums'>{val}</div>
          <div style='font-size:11px; font-weight:600; color:#111827; margin-top:3px'>{label}</div>
          <div style='font-size:10px; color:#9ca3af; margin-top:2px'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:10px; font-size:10px; color:#9ca3af;
                text-align:center; font-style:italic'>
      Signal charts above are illustrative examples only - actual research data is proprietary.
      Statistics (99.74%, 306,600 readings, 67% reduction) are from published peer-reviewed work.
    </div>
    """, unsafe_allow_html=True)

    # ── Publications ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-label">Related Publications</p>', unsafe_allow_html=True)

    journal_pubs = [
        {
            "authors": "Hookoom, T., Bangarigadu, K., Ramgolam, Y.K.",
            "year": "2022",
            "title": "Optimisation of Geographically Deployed PV Parks for Reduction of Intermittency to Enhance Grid Stability",
            "venue": "Renewable Energy Journal",
            "pages": "",
            "doi": "10.1016/j.renene.2022.02.007",
        },
        {

            "authors": "Ramiah, C., Bangarigadu, K., Hookoom, T., Ramgolam, Y.K.",
            "year": "2023",
            "title": "A Novel and Holistic Framework for The Selection of Performance Indicators To Appraise Photovoltaic Systems",
            "venue": "Proceedings of Solar World Congress 2023",
            "pages": "pp. 1–12",
            "doi": "10.18086/swc.2023.08.05",
        },
        {
            "authors": "Ramgolam, Y., Bangarigadu, K., Hookoom, T.",
            "year": "2020",
            "title": "A Robust Methodology for Assessing the Effectiveness of Site Adaptation Techniques for Calibration of Solar Radiation Data",
            "venue": "Journal of Solar Energy Engineering",
            "pages": "143(3)",
            "doi": "10.1115/1.4048547",
        },
        {
            "authors": "Bangarigadu, K., Hookoom, T., Ramgolam, Y., Kune, N.",
            "year": "2020",
            "title": "Analysis of Solar Power and Energy Variability Through Site Adaptation of Satellite Data With Quality Controlled Measured Solar Radiation Data",
            "venue": "Journal of Solar Energy Engineering",
            "pages": "143(3)",
            "doi": "10.1115/1.4048546",
        },
    ]

    book_pubs = [
        {
            "authors": "Hookoom, T., Bangarigadu, K., Ramiah, C., Ramgolam, Y.K.",
            "year": "2024",
            "title": "Strengthening health services with quality in a net zero transition",
            "venue": "The Elgar Companion to Energy and Sustainability",
            "type": "Book Chapter",
            "doi": "10.4337/9781035307494.00027",
        },
    ]

    lcol, rcol = st.columns([3, 2])

    with lcol:
        st.markdown("**Journal Publications & Conference Proceedings - Tavish Hookoom**")
        for i, pub in enumerate(journal_pubs):
            doi_link = f'<a href="https://doi.org/{pub["doi"]}" target="_blank" style="color:#2563eb; font-size:10px; text-decoration:none">DOI ↗</a>' if pub["doi"] else ""
            pages = f" · {pub['pages']}" if pub["pages"] else ""
            st.markdown(f"""
            <div style='background:white; border:1px solid #e4e7ec; border-radius:10px;
                        padding:14px 16px; margin-bottom:10px;
                        box-shadow:0 1px 3px rgba(0,0,0,0.04);
                        border-left:3px solid #2563eb'>
              <div style='font-size:11px; color:#6b7280; margin-bottom:4px'>
                {pub['authors']} ({pub['year']}) {doi_link}
              </div>
              <div style='font-size:12.5px; font-weight:600; color:#111827; margin-bottom:4px; line-height:1.4'>
                {pub['title']}
              </div>
              <div style='font-size:11px; color:#6b7280; font-style:italic'>
                {pub['venue']}{pages}
              </div>
            </div>
            """, unsafe_allow_html=True)

    with rcol:
        st.markdown("**Book Chapter**")
        for pub in book_pubs:
            st.markdown(f"""
            <div style='background:white; border:1px solid #e4e7ec; border-radius:10px;
                        padding:14px 16px; margin-bottom:10px;
                        box-shadow:0 1px 3px rgba(0,0,0,0.04);
                        border-left:3px solid #7c3aed'>
              <div style='font-size:11px; color:#6b7280; margin-bottom:4px'>
                {pub['authors']} ({pub['year']})
                <span style='background:#ede9fe; color:#7c3aed; font-size:9px;
                             font-weight:700; padding:2px 7px; border-radius:10px;
                             margin-left:6px'>{pub['type']}</span>
              </div>
              <div style='font-size:12.5px; font-weight:600; color:#111827; margin-bottom:4px; line-height:1.4'>
                {pub['title']}
              </div>
              <div style='font-size:11px; color:#6b7280; font-style:italic'>
                {pub['venue']}
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#f0f7ff; border:1px solid #bfdbfe; border-radius:10px;
                    padding:14px 16px'>
          <div style='font-size:11px; font-weight:700; color:#1e40af; margin-bottom:6px'>
            Research Summary
          </div>
          <div style='font-size:11px; color:#1e3a5f; line-height:1.7'>
            • 4 journal / conference papers<br>
            • 1 book chapter (Elgar, 2024)<br>
            • Solar World Congress 2023<br>
            • Renewable Energy Journal (Elsevier)<br>
            • Journal of Solar Energy Engineering (ASME)
          </div>
        </div>
        """, unsafe_allow_html=True)
