# app.py — דשבורד אנרגיה ולוגיסטיקה  |  Final Version — Marom-Media
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import time
import requests

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="דשבורד אנרגיה ולוגיסטיקה",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
#  CSS — WHITE-LABEL  |  CORPORATE RTL  |  HIGH CONTRAST
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800;900&display=swap');

/* ── 1. Hide all Streamlit chrome ────────────────────────────── */
#MainMenu,
header[data-testid="stHeader"],
footer,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
.stDeployButton,
button[data-testid="baseButton-headerNoPadding"],
section[data-testid="stSidebar"] { display: none !important; }

/* ── 2. Global base ──────────────────────────────────────────── */
html, body {
    direction: rtl !important;
    font-family: 'Heebo', sans-serif !important;
    background: #f0f4f8 !important;
}

.main .block-container {
    padding: 0.6rem 2rem 2rem !important;
    max-width: 1500px !important;
    direction: rtl !important;
}

/* ── 3. Force RTL on all Streamlit containers ─────────────────── */
section.main > div,
div[data-testid="stAppViewContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="column"],
div.element-container {
    direction: rtl !important;
}

/* ── 4. Typography — all text blocks right-aligned ───────────── */
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown strong, .stMarkdown em,
div[data-testid="stText"],
div[data-testid="stCaptionContainer"],
small, .stCaption {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}

/* ── 5. Widget labels ────────────────────────────────────────── */
label,
div[data-testid="stWidgetLabel"],
div[data-testid="stWidgetLabel"] p,
.stSelectbox > label,
.stNumberInput > label,
.stSlider > label,
.stRadio > label,
.stCheckbox > label {
    direction: rtl !important;
    text-align: right !important;
    width: 100% !important;
    font-family: 'Heebo', sans-serif !important;
    font-weight: 600 !important;
    color: #1a1a2e !important;
}

/* ── 6. Alert / info boxes ───────────────────────────────────── */
div[data-testid="stAlert"],
div[data-testid="stAlert"] p {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}

/* ── 7. Metric widgets ───────────────────────────────────────── */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}
div[data-testid="stMetricValue"] { direction: ltr !important; text-align: right !important; }
div[data-testid="stMetricDelta"]  { direction: ltr !important; text-align: right !important; }

/* ── 8. Expander header ──────────────────────────────────────── */
div[data-testid="stExpanderHeader"],
div[data-testid="stExpanderHeader"] p {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
    font-weight: 700 !important;
    color: #0d1b2a !important;
}
div[data-testid="stExpander"] {
    border: 1px solid #dde3ef !important;
    border-radius: 12px !important;
    background: #f8faff !important;
    margin-bottom: 0.7rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

/* ── 9. Inputs, select, radio ────────────────────────────────── */
div[data-baseweb="select"]   { direction: rtl !important; }
div[data-baseweb="input"]    { direction: rtl !important; }
div[data-testid="stRadio"] > div  { direction: rtl !important; }
div[data-testid="stRadio"] label  { text-align: right !important; }
div[data-testid="stCheckbox"]     { direction: rtl !important; }

/* ── 10. Spinner ─────────────────────────────────────────────── */
div[data-testid="stSpinner"] p {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}

/* ════════════════════════════════════════════════════════════════
   COMPONENT STYLES
   ════════════════════════════════════════════════════════════════ */

/* ── Dashboard header ────────────────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2f50 60%, #1a3a6e 100%);
    color: #fff;
    padding: 1.5rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 0.7rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(13,27,42,0.22);
}
.dash-header h1 {
    font-size: 1.85rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -0.5px;
    direction: rtl;
}
.dash-header .sub  { font-size: 0.86rem; opacity: 0.68; margin-top: 0.25rem; }
.dash-header .meta {
    display: inline-flex;
    gap: 1.4rem;
    align-items: center;
    margin-top: 0.45rem;
    font-size: 0.74rem;
    opacity: 0.5;
    direction: ltr;
    flex-wrap: wrap;
    justify-content: center;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    display: inline-block; margin-left: 4px;
    animation: blink 2s infinite;
}
.status-dot.live { background: #4ade80; box-shadow: 0 0 6px #4ade80; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }

/* ── Section titles ──────────────────────────────────────────── */
.sec-title {
    border-right: 5px solid #0d1b2a;
    padding: 0.42rem 0.85rem;
    background: #e8edf8;
    border-radius: 0 8px 8px 0;
    font-weight: 800;
    font-size: 0.93rem;
    color: #0d1b2a;
    margin: 1rem 0 0.45rem;
    direction: rtl;
    text-align: right;
    display: block;
}

/* ── Price alert banners ─────────────────────────────────────── */
.alert-banner {
    background: #fff5f5;
    border: 2px solid #dc2626;
    border-radius: 10px;
    padding: 0.7rem 1.1rem;
    margin: 0.3rem 0;
    direction: rtl;
    text-align: right;
    font-size: 0.88rem;
    font-weight: 600;
    color: #7f1d1d;
    box-shadow: 0 2px 8px rgba(220,38,38,0.10);
    font-family: 'Heebo', sans-serif;
}

/* ── KPI cards ───────────────────────────────────────────────── */
.kpi-card {
    background: #fff;
    border-radius: 14px;
    padding: 0.95rem 1.1rem 0.65rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-right: 5px solid #0d1b2a;
    direction: rtl;
    text-align: right;
    height: 100%;
    box-sizing: border-box;
}
.kpi-lbl  { font-size: 0.74rem; color: #64748b; font-weight: 600; margin-bottom: 0.1rem; }
.kpi-val  {
    font-size: 1.85rem; font-weight: 900; color: #0d1b2a;
    line-height: 1.05; direction: ltr; text-align: right;
    letter-spacing: -0.5px;
}
.kpi-row  {
    display: flex; align-items: center;
    justify-content: space-between; margin-top: 0.15rem;
}
.kpi-unit { font-size: 0.7rem; color: #94a3b8; }
.kpi-up   { font-size: 0.78rem; font-weight: 700; color: #dc2626; }
.kpi-dn   { font-size: 0.78rem; font-weight: 700; color: #16a34a; }
.kpi-flat { font-size: 0.78rem; color: #94a3b8; }
.kpi-spark { margin-top: 0.35rem; line-height: 0; }

/* ── Comparison table ────────────────────────────────────────── */
.cmp-wrap {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.cmp-table {
    width: 100%; direction: rtl;
    border-collapse: collapse;
    font-size: 0.86rem;
    background: white;
    font-family: 'Heebo', sans-serif;
}
.cmp-table thead th {
    background: #0d1b2a; color: #fff;
    padding: 0.6rem 1rem; text-align: center;
    font-weight: 700; font-size: 0.8rem;
}
.cmp-table thead th:first-child { text-align: right; padding-right: 1.2rem; }
.cmp-table tbody td {
    padding: 0.55rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    text-align: center;
}
.cmp-table tbody td:first-child { text-align: right; font-weight: 700; color: #0d1b2a; }
.cmp-table tbody tr:last-child td { border-bottom: none; }
.cmp-table tbody tr:hover { background: #f8faff; }
.ch-up   { color: #dc2626; font-weight: 700; }
.ch-dn   { color: #16a34a; font-weight: 700; }
.ch-flat { color: #94a3b8; }

/* ── Calculator section title ────────────────────────────────── */
.calc-title {
    font-size: 0.93rem; font-weight: 800; color: #0d1b2a;
    direction: rtl; text-align: right; margin-bottom: 0.5rem;
}

/* ── Shipping summary box ────────────────────────────────────── */
.ship-summary {
    border-radius: 9px; padding: 0.75rem 1rem;
    margin-top: 0.5rem; direction: rtl; text-align: right;
    font-size: 0.9rem; font-weight: 500;
    border-right-width: 4px; border-right-style: solid;
}
.ship-summary.up   { background:#fff5f5; color:#7f1d1d; border-right-color:#dc2626; }
.ship-summary.down { background:#f0fdf4; color:#14532d; border-right-color:#16a34a; }

/* ── Buttons ─────────────────────────────────────────────────── */
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(135deg, #0d1b2a, #1a3a6e) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Heebo', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.3rem !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 2px 8px rgba(13,27,42,0.18) !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Custom footer ───────────────────────────────────────────── */
.custom-footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.76rem;
    padding: 1.2rem 0 0.4rem;
    font-family: 'Heebo', sans-serif;
    letter-spacing: 0.2px;
}
.custom-footer strong { color: #64748b; font-weight: 600; }
.custom-footer a { color: #64748b; text-decoration: none; }
.custom-footer a:hover { text-decoration: underline; }

/* ── Divider ─────────────────────────────────────────────────── */
hr { border-color: #dde3ef !important; margin: 1.2rem 0 0.3rem !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  RESPONSIVE CSS — MOBILE & TABLET
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Tablet: up to 900px ─────────────────────────────────────── */
@media screen and (max-width: 900px) {

    .main .block-container {
        padding: 0.4rem 1rem 2rem !important;
    }

    /* Stack all column groups */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 0.6rem !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: none !important;
    }

    /* Header */
    .dash-header { padding: 1.1rem 1.2rem !important; border-radius: 12px !important; }
    .dash-header h1  { font-size: 1.45rem !important; }
    .dash-header .sub { font-size: 0.8rem !important; }
    .dash-header .meta {
        flex-direction: column !important;
        gap: 0.25rem !important;
        font-size: 0.72rem !important;
    }

    /* KPI cards — 2-column grid on tablet */
    .kpi-card { padding: 0.85rem 1rem 0.6rem !important; }
    .kpi-val  { font-size: 1.6rem !important; }
    .kpi-lbl  { font-size: 0.72rem !important; }

    /* Section titles */
    .sec-title { font-size: 0.88rem !important; }

    /* Comparison table — horizontal scroll */
    .cmp-wrap  { overflow-x: auto !important; -webkit-overflow-scrolling: touch; }
    .cmp-table { min-width: 480px !important; font-size: 0.82rem !important; }

    /* Calculators */
    .calc-title { font-size: 0.88rem !important; }

    /* Alerts */
    .alert-banner { font-size: 0.84rem !important; padding: 0.65rem 0.9rem !important; }

    /* Expander */
    div[data-testid="stExpander"] { border-radius: 10px !important; }
}

/* ── Mobile: up to 480px ─────────────────────────────────────── */
@media screen and (max-width: 480px) {

    .main .block-container {
        padding: 0.3rem 0.5rem 1.5rem !important;
    }

    /* Header — compact */
    .dash-header { padding: 0.9rem 1rem !important; border-radius: 10px !important; }
    .dash-header h1  { font-size: 1.15rem !important; letter-spacing: 0 !important; }
    .dash-header .sub { display: none !important; }   /* hide tagline on very small */

    /* KPI cards */
    .kpi-card { padding: 0.7rem 0.8rem 0.45rem !important; border-radius: 10px !important; }
    .kpi-val  { font-size: 1.4rem !important; letter-spacing: 0 !important; }
    .kpi-lbl  { font-size: 0.7rem !important; }
    .kpi-unit { font-size: 0.67rem !important; }
    .kpi-up, .kpi-dn, .kpi-flat { font-size: 0.72rem !important; }

    /* Section titles */
    .sec-title {
        font-size: 0.82rem !important;
        padding: 0.38rem 0.7rem !important;
        margin: 0.75rem 0 0.35rem !important;
    }

    /* Comparison table */
    .cmp-table { font-size: 0.78rem !important; min-width: 420px !important; }
    .cmp-table thead th { padding: 0.5rem 0.6rem !important; font-size: 0.74rem !important; }
    .cmp-table tbody td { padding: 0.45rem 0.6rem !important; }

    /* Calculators */
    .calc-title   { font-size: 0.82rem !important; }
    .ship-summary { font-size: 0.8rem !important; padding: 0.6rem 0.8rem !important; }

    /* Alert banners */
    .alert-banner { font-size: 0.78rem !important; }

    /* Expander */
    div[data-testid="stExpanderHeader"] p { font-size: 0.84rem !important; }

    /* Buttons */
    div.stButton > button,
    div.stDownloadButton > button { font-size: 0.84rem !important; padding: 0.45rem 1rem !important; }

    /* Custom footer */
    .custom-footer { font-size: 0.7rem !important; padding: 0.8rem 0 0.3rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  CONSTANTS — 4 ASSETS
# ══════════════════════════════════════════════════════════════════
ASSETS = {
    "🛢️ נפט ברנט":  ("BZ=F",     "$/חבית", "#c0392b"),
    "🛢️ נפט WTI":   ("CL=F",     "$/חבית", "#e67e22"),
    "💵 דולר/שקל":  ("USDILS=X", "₪",      "#1d4ed8"),
    "💶 אירו/שקל":  ("EURILS=X", "₪",      "#6d28d9"),
}
PERIOD_OPTS = {"7 ימים": 7, "30 ימים": 30, "90 ימים": 90}

# ══════════════════════════════════════════════════════════════════
#  DATA LAYER
# ══════════════════════════════════════════════════════════════════
_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
_MAX_RETRIES = 3
_RETRY_DELAY = 2.0  # seconds between attempts

@st.cache_data(ttl=300)
def fetch_series(ticker: str, days: int = 380) -> pd.Series:
    """
    Fetch historical close prices for `ticker`.
    Uses a browser User-Agent and retries up to _MAX_RETRIES times
    so Streamlit Cloud IP blocks / transient Yahoo Finance errors
    don't silently return empty data.
    """
    end   = datetime.today()
    start = end - timedelta(days=days + 20)

    session = requests.Session()
    session.headers.update({"User-Agent": _UA})

    df = pd.DataFrame()
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=True,
                session=session,
            )
            if not df.empty:
                break          # success — exit retry loop
        except Exception:
            pass               # swallow; retry or fall through

        if attempt < _MAX_RETRIES:
            time.sleep(_RETRY_DELAY)

    if df.empty:
        return pd.Series(dtype=float)

    col = "Close" if "Close" in df.columns else df.columns[0]
    s   = df[col].squeeze()
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    s.index = pd.to_datetime(s.index).tz_localize(None)
    return s.dropna().sort_index()

def safe_val(s: pd.Series, offset: int = 0):
    try:
        return float(s.iloc[-(1 + offset)])
    except Exception:
        return None

def pct_diff(new_val, old_val):
    if new_val is None or old_val is None or old_val == 0:
        return None
    return ((new_val - old_val) / old_val) * 100

# ══════════════════════════════════════════════════════════════════
#  SPARKLINE  (inline SVG — 14-day mini-chart)
# ══════════════════════════════════════════════════════════════════
def sparkline_svg(s: pd.Series, color: str, w: int = 90, h: int = 34) -> str:
    vals = [float(v) for v in s.dropna().tail(14).values]
    if len(vals) < 2:
        return f'<div style="height:{h}px"></div>'
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return f'<div style="height:{h}px"></div>'
    pad = 3
    n   = len(vals)
    pts = []
    for i, v in enumerate(vals):
        x = round((i / (n - 1)) * (w - pad * 2) + pad, 1)
        y = round((h - pad * 2) - ((v - mn) / (mx - mn)) * (h - pad * 2) + pad, 1)
        pts.append((x, y))
    poly = " ".join(f"{x},{y}" for x, y in pts)
    fill = f"{pts[0][0]},{h} " + poly + f" {pts[-1][0]},{h}"
    lx, ly = pts[-1]
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" style="display:block;overflow:hidden;border-radius:4px">'
        f'<polygon points="{fill}" fill="rgba({r},{g},{b},0.10)"/>'
        f'<polyline points="{poly}" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle cx="{lx}" cy="{ly}" r="2.8" fill="{color}"/>'
        f'</svg>'
    )

# ══════════════════════════════════════════════════════════════════
#  HTML HELPERS
# ══════════════════════════════════════════════════════════════════
def kpi_html(label: str, value, unit: str, pct, spark: str) -> str:
    if value is None:
        return (
            f'<div class="kpi-card">'
            f'<div class="kpi-lbl">{label}</div>'
            f'<div class="kpi-val">—</div>'
            f'</div>'
        )
    fmt = f"{value:,.3f}" if (unit == "₪" and value < 10) else f"{value:,.2f}"
    if pct is None:
        badge = '<span class="kpi-flat">—</span>'
    elif pct > 0:
        badge = f'<span class="kpi-up">▲&nbsp;{pct:.2f}%</span>'
    else:
        badge = f'<span class="kpi-dn">▼&nbsp;{abs(pct):.2f}%</span>'
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-lbl">{label}</div>'
        f'<div class="kpi-val">{fmt}</div>'
        f'<div class="kpi-row"><span class="kpi-unit">{unit}</span>{badge}</div>'
        f'<div class="kpi-spark">{spark}</div>'
        f'</div>'
    )

def ch_cell(base, hist) -> str:
    p = pct_diff(base, hist)
    if p is None:
        return '<span class="ch-flat">—</span>'
    if p > 0:
        return f'<span class="ch-up">▲&nbsp;{abs(p):.1f}%</span>'
    if p < 0:
        return f'<span class="ch-dn">▼&nbsp;{abs(p):.1f}%</span>'
    return '<span class="ch-flat">0.0%</span>'

def comparison_table_html(data_map: dict) -> str:
    rows = ""
    for label, (ticker, unit, _) in ASSETS.items():
        s = data_map[ticker]
        if len(s) < 2:
            rows += (
                f'<tr><td>{label}</td>'
                f'<td colspan="4" style="color:#94a3b8;text-align:center">נתונים לא זמינים</td></tr>'
            )
            continue
        cur = safe_val(s, 0)
        w1  = safe_val(s, min(7,   len(s) - 1))
        m1  = safe_val(s, min(22,  len(s) - 1))
        y1  = safe_val(s, min(252, len(s) - 1))
        fmt = (f"{cur:.3f}&nbsp;{unit}"
               if (cur and unit == "₪" and cur < 10)
               else f"{cur:.2f}&nbsp;{unit}" if cur else "—")
        rows += (
            f"<tr><td>{label}</td><td>{fmt}</td>"
            f"<td>{ch_cell(cur, w1)}</td>"
            f"<td>{ch_cell(cur, m1)}</td>"
            f"<td>{ch_cell(cur, y1)}</td></tr>"
        )
    return (
        '<div class="cmp-wrap">'
        '<table class="cmp-table"><thead><tr>'
        '<th>נכס</th><th>מחיר נוכחי</th>'
        '<th>מול שבוע שעבר</th><th>מול חודש שעבר</th><th>מול שנה שעברה</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>'
    )

# ══════════════════════════════════════════════════════════════════
#  CHART BUILDER
# ══════════════════════════════════════════════════════════════════
def trend_chart(series: pd.Series, name: str, color: str,
                days: int, show_ma: bool) -> go.Figure:
    s = series.tail(days)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=s.index, y=s.values, mode="lines", name=name,
        line=dict(color=color, width=2.5),
        fill="tozeroy", fillcolor=f"rgba({r},{g},{b},0.09)",
        hovertemplate="%{y:.3f}<extra>" + name + "</extra>",
    ))
    if show_ma and len(s) >= 7:
        ma7 = s.rolling(7).mean()
        fig.add_trace(go.Scatter(
            x=ma7.index, y=ma7.values, mode="lines",
            name="ממוצע 7 ימים",
            line=dict(color="#f59e0b", width=1.8, dash="dash"),
            hovertemplate="%{y:.3f}<extra>MA7</extra>",
        ))
    if show_ma and len(s) >= 30:
        ma30 = s.rolling(30).mean()
        fig.add_trace(go.Scatter(
            x=ma30.index, y=ma30.values, mode="lines",
            name="ממוצע 30 ימים",
            line=dict(color="#ef4444", width=1.8, dash="dot"),
            hovertemplate="%{y:.3f}<extra>MA30</extra>",
        ))
    fig.update_layout(
        margin=dict(l=4, r=4, t=14, b=4), height=270,
        legend=dict(
            orientation="h", y=1.16, x=0,
            font=dict(size=10, family="Heebo, sans-serif"),
            bgcolor="rgba(255,255,255,0.9)",
        ),
        xaxis=dict(
            showgrid=True, gridcolor="#f1f5f9",
            tickfont=dict(size=10, family="Heebo, sans-serif"),
            tickformat="%d/%m",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#f1f5f9",
            tickfont=dict(size=10, family="Heebo, sans-serif"),
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        font=dict(family="Heebo, sans-serif", size=11),
    )
    return fig

# ══════════════════════════════════════════════════════════════════
#  EXCEL EXPORT
# ══════════════════════════════════════════════════════════════════
def build_excel(data_map: dict) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        for label, (ticker, unit, _) in ASSETS.items():
            s = data_map[ticker]
            if len(s) == 0:
                continue
            df = s.reset_index()
            df.columns = ["תאריך", f"מחיר ({unit})"]
            df["תאריך"] = pd.to_datetime(df["תאריך"]).dt.strftime("%Y-%m-%d")
            safe_label  = label.replace("/", "-").replace('"', "'")[:28]
            df.to_excel(writer, sheet_name=safe_label, index=False)
    return buf.getvalue()

# ══════════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════════
with st.spinner("טוען נתונים עדכניים מהשוק..."):
    data_map = {t: fetch_series(t) for _, (t, _, _) in ASSETS.items()}

# Convenience references to current prices
brent_cur = safe_val(data_map["BZ=F"])
wti_cur   = safe_val(data_map["CL=F"])
usd_cur   = safe_val(data_map["USDILS=X"])
eur_cur   = safe_val(data_map["EURILS=X"])

# ══════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════
now    = datetime.now()
now_he = now.strftime("%d/%m/%Y  %H:%M")
st.markdown(
    f'<div class="dash-header">'
    f'<h1>⚡ דשבורד אנרגיה ולוגיסטיקה</h1>'
    f'<div class="sub">מעקב מחירי נפט, מטבעות ועלויות לוגיסטיקה בזמן אמת</div>'
    f'<div class="meta">'
    f'  <span><span class="status-dot live"></span>נתונים חיים</span>'
    f'  <span>עדכון: {now_he}</span>'
    f'  <span>מקור: Yahoo Finance</span>'
    f'</div></div>',
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════
#  SETTINGS EXPANDER
# ══════════════════════════════════════════════════════════════════
with st.expander("⚙️  הגדרות תצוגה והתראות מחיר", expanded=False):
    s1, s2, s3 = st.columns([2, 2, 1])
    with s1:
        period_label = st.selectbox("תקופת תרשים", list(PERIOD_OPTS.keys()), index=1)
        period_days  = PERIOD_OPTS[period_label]
    with s2:
        show_ma = st.checkbox("הצג ממוצעים נעים (MA7 / MA30)", value=True)
    with s3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄  רענן"):
            st.cache_data.clear()
            st.rerun()

    st.markdown("**🔔  ספי התראות מחיר**")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        alert_brent = st.number_input("ברנט — התרע מעל ($)",     value=90.0, step=1.0, format="%.1f")
    with a2:
        alert_wti   = st.number_input("WTI — התרע מעל ($)",      value=85.0, step=1.0, format="%.1f")
    with a3:
        alert_usd   = st.number_input("דולר/שקל — התרע מעל (₪)", value=3.80, step=0.05, format="%.2f")
    with a4:
        alert_eur   = st.number_input("אירו/שקל — התרע מעל (₪)", value=4.20, step=0.05, format="%.2f")
    st.caption("⏱️  הנתונים מתרעננים אוטומטית כל 5 דקות  ·  מקור: Yahoo Finance")

# ══════════════════════════════════════════════════════════════════
#  PRICE ALERT BANNERS
# ══════════════════════════════════════════════════════════════════
def _alert(html: str) -> None:
    st.markdown(f'<div class="alert-banner">{html}</div>', unsafe_allow_html=True)

# Each block is guarded independently — f-strings only evaluated when
# the price value is confirmed not None, preventing TypeError on fetch failure.
if brent_cur is not None and brent_cur > alert_brent:
    _alert(
        f'🚨 <strong>נפט ברנט</strong> עומד על '
        f'${brent_cur:.2f}/חבית — מעל ספף ההתראה (${alert_brent:.1f})'
    )
if wti_cur is not None and wti_cur > alert_wti:
    _alert(
        f'🚨 <strong>נפט WTI</strong> עומד על '
        f'${wti_cur:.2f}/חבית — מעל ספף ההתראה (${alert_wti:.1f})'
    )
if usd_cur is not None and usd_cur > alert_usd:
    _alert(
        f'🚨 <strong>דולר/שקל</strong> עומד על '
        f'₪{usd_cur:.4f} — מעל ספף ההתראה (₪{alert_usd:.2f})'
    )
if eur_cur is not None and eur_cur > alert_eur:
    _alert(
        f'🚨 <strong>אירו/שקל</strong> עומד על '
        f'₪{eur_cur:.4f} — מעל ספף ההתראה (₪{alert_eur:.2f})'
    )

# ══════════════════════════════════════════════════════════════════
#  KPI CARDS  (with 14-day sparklines)
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">📊  מחירים עכשוויים</div>', unsafe_allow_html=True)

kpi_cols = st.columns(4, gap="small")
for col, (label, (ticker, unit, color)) in zip(kpi_cols, ASSETS.items()):
    s   = data_map[ticker]
    cur = safe_val(s, 0)
    prv = safe_val(s, 1)
    pct = pct_diff(cur, prv)
    svg = sparkline_svg(s, color)
    with col:
        st.markdown(kpi_html(label, cur, unit, pct, svg), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TREND CHARTS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">📈  תרשימי מגמה</div>', unsafe_allow_html=True)

# Row 1 — oil (2 equal columns)
oil_items = list(ASSETS.items())[:2]
c1, c2 = st.columns(2, gap="medium")
for col, (label, (ticker, unit, color)) in zip([c1, c2], oil_items):
    s   = data_map[ticker]
    cur = safe_val(s, 0)
    sub = f"${cur:.2f} {unit}" if cur else "—"
    with col:
        st.markdown(f"**{label}** &nbsp;—&nbsp; {sub}")
        if len(s) >= 2:
            st.plotly_chart(
                trend_chart(s, label, color, period_days, show_ma),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.warning("נתונים לא זמינים כרגע")

# Row 2 — currencies (2 equal columns)
cur_items = list(ASSETS.items())[2:]
c3, c4 = st.columns(2, gap="medium")
for col, (label, (ticker, unit, color)) in zip([c3, c4], cur_items):
    s   = data_map[ticker]
    cur = safe_val(s, 0)
    sub = f"₪{cur:.4f}" if cur else "—"
    with col:
        st.markdown(f"**{label}** &nbsp;—&nbsp; {sub}")
        if len(s) >= 2:
            st.plotly_chart(
                trend_chart(s, label, color, period_days, show_ma),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.warning("נתונים לא זמינים כרגע")

# ══════════════════════════════════════════════════════════════════
#  HISTORICAL COMPARISON TABLE
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">🗂️  ניתוח השוואתי — היום מול עבר</div>', unsafe_allow_html=True)
st.markdown(comparison_table_html(data_map), unsafe_allow_html=True)
st.caption("ירוק ▼ = ירידת מחיר (חיסכון)  ·  אדום ▲ = עלייה (עלות נוספת)")

# ══════════════════════════════════════════════════════════════════
#  CALCULATORS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">🧮  מחשבונים מהירים</div>', unsafe_allow_html=True)

calc_l, calc_r = st.columns(2, gap="large")

# ── Currency converter ────────────────────────────────────────────
with calc_l:
    st.markdown('<div class="calc-title">💱 מחשבון המרת מטבע</div>', unsafe_allow_html=True)
    fx_options = {
        "דולר אמריקאי (USD)": ("USDILS=X", "$",  "USD"),
        "אירו (EUR)":          ("EURILS=X", "€",  "EUR"),
    }
    chosen_fx               = st.selectbox("בחר מטבע", list(fx_options.keys()), key="fx_sel")
    fx_ticker, fx_sym, fx_code = fx_options[chosen_fx]
    fx_rate                 = safe_val(data_map[fx_ticker])
    amount_fx               = st.number_input(
        "סכום להמרה", min_value=0.0, value=1000.0, step=100.0, key="fx_amt"
    )
    direction               = st.radio(
        "כיוון המרה",
        [f"{fx_code} ← ₪", f"₪ ← {fx_code}"],
        horizontal=True, key="fx_dir"
    )
    if fx_rate and fx_rate > 0:
        if f"₪ ← {fx_code}" in direction:
            result = amount_fx / fx_rate
            st.success(f"₪{amount_fx:,.2f}  =  **{fx_sym}{result:,.2f}**  ·  שער: ₪{fx_rate:.4f}")
        else:
            result = amount_fx * fx_rate
            st.success(f"{fx_sym}{amount_fx:,.2f}  =  **₪{result:,.2f}**  ·  שער: ₪{fx_rate:.4f}")
    else:
        st.warning("שער חליפין לא זמין כרגע")

# ── Shipping cost calculator ──────────────────────────────────────
with calc_r:
    st.markdown('<div class="calc-title">🚛 מחשבון השפעת הנפט על עלות הובלה</div>',
                unsafe_allow_html=True)

    live_brent   = round(float(brent_cur), 2) if brent_cur else 85.0
    rate_display = f"₪{usd_cur:.4f}" if usd_cur else "לא זמין"
    st.caption(
        f"שער דולר/שקל חי: **{rate_display}**  ·  "
        f"מחיר ברנט נוכחי: **${live_brent:.2f}**"
    )

    inp1, inp2 = st.columns(2)
    with inp1:
        baseline_oil = st.number_input(
            "מחיר נפט בסיס / ייחוס ($/חבית)",
            value=round(live_brent - 5, 1),
            step=0.5, key="ship_baseline",
            help="המחיר שעליו תכננת את עלות ההובלה"
        )
    with inp2:
        current_oil = st.number_input(
            "מחיר נפט נוכחי ($/חבית)",
            value=live_brent,
            step=0.5, key="ship_current",
            help="מתעדכן אוטומטית — ניתן לשנות ידנית"
        )

    base_cost = st.number_input(
        "עלות הובלה בסיס (₪) — לפי מחיר הייחוס",
        value=12000.0, step=500.0, key="ship_cost"
    )
    fuel_pct = st.slider(
        "% דלק מתוך עלות ההובלה הכוללת",
        min_value=5, max_value=60, value=30, key="ship_pct"
    )

    if baseline_oil > 0:
        oil_chg_pct   = ((current_oil - baseline_oil) / baseline_oil) * 100
        delta_ils     = base_cost * (fuel_pct / 100) * (oil_chg_pct / 100)
        new_cost_ils  = base_cost + delta_ils
        oil_delta_usd = current_oil - baseline_oil
        oil_delta_ils = (oil_delta_usd * usd_cur) if usd_cur else None

        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric(
            "מחיר נפט נוכחי",
            f"${current_oil:.2f}",
            delta=f"{oil_delta_usd:+.2f} $/חבית"
        )
        m2.metric(
            "השפעה על עלות הובלה",
            f"₪{abs(delta_ils):,.0f}",
            delta=f"{'עלייה' if delta_ils > 0 else 'חיסכון'}"
        )
        m3.metric(
            "עלות הובלה מעודכנת",
            f"₪{new_cost_ils:,.0f}",
            delta=f"{delta_ils:+,.0f} ₪"
        )

        # ILS context
        if oil_delta_ils is not None:
            st.caption(
                f"שינוי מחיר הנפט: ${abs(oil_delta_usd):.2f}/חבית"
                f" = ₪{abs(oil_delta_ils):.2f}/חבית "
                f"(לפי שער {rate_display})"
            )

        # Hebrew summary sentence
        direction_he = "עליית"   if delta_ils > 0 else "ירידת"
        oil_dir_he   = "עלה"     if oil_chg_pct > 0 else "ירד"
        css_cls      = "up"      if delta_ils > 0 else "down"
        icon         = "🔴"      if delta_ils > 0 else "🟢"
        summary      = (
            f"{icon} עלות ההובלה <strong>השתנתה ב-₪{abs(delta_ils):,.0f}</strong> "
            f"עקב {direction_he} מחיר הנפט — "
            f"הנפט {oil_dir_he} {abs(oil_chg_pct):.1f}% "
            f"מ-${baseline_oil:.1f} ל-${current_oil:.1f}."
        )
        st.markdown(
            f'<div class="ship-summary {css_cls}">{summary}</div>',
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════
#  EXPORT TO EXCEL
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-title">📥  ייצוא נתונים</div>', unsafe_allow_html=True)

exp_c, info_c = st.columns([1, 3], gap="medium")
with exp_c:
    excel_bytes = build_excel(data_map)
    fname = f"energy_dashboard_{now.strftime('%Y%m%d_%H%M')}.xlsx"
    st.download_button(
        label="📥  ייצוא לאקסל — כל הנכסים",
        data=excel_bytes,
        file_name=fname,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
with info_c:
    st.info(
        "הקובץ כולל גיליון נפרד לכל נכס (ברנט, WTI, דולר/שקל, אירו/שקל) "
        "עם היסטוריית מחירים מלאה — מוכן לשילוב בדוחות COGS ולדיווח להנהלה."
    )

# ══════════════════════════════════════════════════════════════════
#  CUSTOM FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<div class="custom-footer">'
    'Developed by <strong>Marom Cohen</strong> | Marom-Media'
    '</div>',
    unsafe_allow_html=True,
)
