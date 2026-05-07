"""
采姸服飾 Meta 廣告 × GA4 即時報表 v5.1
"""
import math
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sys, os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

LOGO_B64 = "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"

META_LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAE1ElEQVR4nO1WW2yURRQ+Z2b+23Z7BQlCCykoxgLxUuNTBUzkiXiLoW/EB3D1QfBCVBDKdmlroolCokIrhoTIC6zxwWDik9h4CQ9EBbSJhmChmipUtu122/82c8zM/svNVtA3Ek7y55+d/8z55nzntgC35GYX/PfPhJBNdHJAAEjTqmWJmXcnEOAMOteVtcSvu0f6QglYRQ5rHZrRETHjjXMoWzN91knx2BJQgPOm/NNnD6BfNoZkdBCVhnW7Jpuk69WmZWGo0I5jyW3KetcITutFHqX1zOC6mDtbSEZ3GaK4dYZj/H7c27TbeNGO0suW5vmOvQuIt5ONgEF8gRH0tsVf7+zPrZIJBM0MmICJDWe2x059FwADkFOAOnwiZd4sGj8Y9y1Y53WX5vvM7qe0WIyF4BgQXQRkq6nOtlgh+vQhsp7qHwCCPKgrQfFaMJ4ZXCN51REgAlT+F4ypHkGkJLFNxN0nQXjAw4t7o6bGpZTmK9homKFOZ5+2aPf4LZHkeaoVLbwQviE7nW0VNq4BTIL89KDDbDihnIY70R89fvf8YttAbllYUbYzZz9UdvV6lAGoOXMBMdgRd7pdxmgBGDyLkbUzWB4JdgwIhB3K5WHO/SXJCR1vzZlOki+5dpunrEeVW78E5aTiQm0yYGt/tGHlUaEZCD9YuIFFpa+Q81iMDE9WFQoflZkB0GDQR1a0wznF/egg1Ag7YphJ7nopk8uLgVWGY+K8HbxaAoi/jXubj5mb5ZeF0J8kQB+l4jkNNcBQILNSYeC/p8NwKSz1oHSpIIoDWDImH2/tIwtyGFdYZGaRR7kwSy4J8QAIQHTcI4lCwgCU4zvk96iG1D1k4zALiorcujXe8+eeMKDa03ZdQEiz0tYJKAUXgPM7To0EixMbCWCy+CMYawQh5iNIQNv63mSWzjJtKIex6C49KFPWRizJCad+1iPA8DsARiTp7duzv6fA8AqmGfz5CpYA4WdKcZASFpn9pRXAgfJCMpwNbpUF5BPjfPhy9gKszJKQMd8DVZwzRbsntuEAMOjAoIho1ywaPR90QL5dGibaDSsIQOdB9xzA2cbOTxXAiliWACEAGBJyFRnPWsDSKf0NC7ZQjdOKo+G5Oke8BZnj1uSe5s9B+XkdKSW8l1Mv/HaviVXjkA1ZQuAs0HBXYZgfLZVdNgIQxZD2mHTsJhOXHPqiK1whBd8OMQAyePWv17AI0Gqoc5m7maKJcWV5Voxif2vmuAW7FkyZElC0CGIElDSSUGpwRHkKEIYAZxDDQRLYrCLWI7rDCaVogSR6lzzLYeP+J6rTO5QUcgQF4oV845Cz8dxm5NY+Euy+k3bzx2LLaDcI3iaFdT+WotD2nB+mypQawHLBJ92A5cLnVNraC4HmiTS9AA4AlqKBGstqG/Nh7KoRlD0qIPdwbL80vE+l524gioBIAgkXqBqATwT7Zae7vtLFLvOrW0+WmMravWwi6EBQ54FiQBX7zI8+c2W0emwrFsq96YpmrBt0llj4ztwMBmNvgopHQFeGiiaxGByq84ovmlo+rPvpdM07GSk1WWqYqoaFLPSLweve6Uq6X2+4preO3xbUVDey2B8NOrxf4YZkuiGrn/96LqsH8z/PTW9IA3RW/lqUm+4NCf3Pc7fkppK/AdqbUsNFGVjBAAAAAElFTkSuQmCC"
GA4_LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAC/0lEQVR4nMWWz4sURxTHP6+6e2Z2Zt2IZEEUyUHwJBjWUy4hghKEBAkiCIKQi8lF/LF6ymF2QMhBIigIiv+BP0BySw5JJLkGEXFBvQR/xCALq7vrdk93Vz2pmtl1NzG6g60+aPpHvXqfV6+qvtVChaaKiKAzFxkdSjiJskuhGUVMZimd1l6uSpUwf5++xMiw4ZdkmLFiLnynVgOrOJuzz1QF5DciP7qm4UCymrHuDLmHeevmWANGhTNVAnumfEyOAxZjC0R5jhphtDpg34wshy1CBXEOrRz4KvPQdwr09s6B8aAdtB2SXEjUSSfM2dsBXtxDJB2sBy1NYBBoPKCK2AdH2RQnfIpgsoI/pMNk2PQTFc6h+lEIen+ciXrCzWbChWbM+VbMjb+OcMK3sa6nNG8M/LVN7Et2/xj7R4dpZ5bkSUrpr8xi1o7w3b2j7JNvKF5LWwnws/58qfLtfI5TxYoQ+0sVlxU4hK+pag6lvyAERqwuT9BvZNtLurXwzfVF/I33oQjuZZGk37bSOGaljtqL/fK214xqqb1fadNXjKJSoLYx6lUkMHtbYZAyDQTUvjTJJWxfJ9nWofSb+W2MOPawu4f4ZPUQ449SNj86TiaGn9KM7+U0TxZ+jCoDPhjnyyTmSiMmcQXhhPygzpbSsn3qINuAWSo044SzIiTTKUVe9pTjnzm6H7YYm69zIJS2X+r/tRVWQEGNETakRfjBSfwJIIIxEBWWUmFriNcJkjbr4f8ur2p4j5bh+a8QeD/xBVTl4VCCWA3nXDAHrhYRR8KtxSiG35sJ4rV0SRDr+wJ3luBukoSKLEKdYuv14HfPoBz2HVu1F1muGaI29YzbYjnnF41frQ5OT6c8HGlQ86Xxfv55tsvjwnHC+3jfeoPzxVMm66uoLcRrNIiso1DDQbPhBy5nJV+pcj0S8tgwkxZcVseO9aeYCj3ayEcn+bss2VmUXIuFIhLm85Kf51J2bDzFnYl2OIRFvmC6SPncdrliIp6JIXfKn2XGrsZufnwOrCs6kuudYeAAAAAASUVORK5CYII="

st.set_page_config(
    page_title="采姸 CHAI YAN｜廣告報表",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""<style>
#MainMenu, footer, [data-testid="stToolbar"] { display:none !important; }
.main .block-container { padding: 1rem 2rem 3rem; max-width: 100%; }
[data-testid="column"] > div:first-child { padding: 0 !important; }

/* Section headers */
.sec-hd {
    font-size: 22px; font-weight: 800; color: #2D1F0F;
    letter-spacing: -.01em;
    margin: 20px 0 14px; display: flex; align-items: center; gap: 12px;
}
.sec-hd::after {
    content: ''; flex: 1; height: 2px;
    background: linear-gradient(to right, #DDD0B8, transparent);
}

/* Tab navigation */
.stTabs [data-baseweb="tab-list"] {
    background: transparent; gap: 0;
    border-bottom: 2px solid #DDD0B8; padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8B7355 !important;
    font-size: 20px !important; font-weight: 700 !important;
    padding: 12px 36px !important;
    border: none !important; border-radius: 0 !important;
    letter-spacing: -.01em !important;
}
.stTabs [aria-selected="true"] {
    color: #1F2937 !important;
    border-bottom: 3px solid #1F2937 !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #1F2937 !important; }
.stTabs [data-baseweb="tab-highlight"] { background: #1F2937 !important; height: 3px !important; }
.stTabs [data-baseweb="tab-border"] { background: #DDD0B8 !important; }

/* First tab = Meta (blue left border when active) */
.stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]:nth-child(1)[aria-selected="true"] {
    color: #1877F2 !important;
    border-bottom: 3px solid #1877F2 !important;
}
/* Second tab = GA4 (orange when active) */
.stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]:nth-child(2)[aria-selected="true"] {
    color: #E8710A !important;
    border-bottom: 3px solid #E8710A !important;
}


.stButton > button {
    background: #374151; color: white; border: none;
    border-radius: 8px; font-weight: 600; font-size: 13px;
    height: 36px; width: 100%;
}
.stButton > button:hover { background: #1F2937; }

.dash-footer {
    text-align: center; padding: 24px 0 8px; color: #8B7355;
    font-size: 12px; border-top: 1px solid #DDD0B8; margin-top: 24px;
}

[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
[data-testid="stPlotlyChart"] { margin: 0 !important; }

/* KPI Cards */
.kpi-grid { display:grid; gap:12px; padding:2px 0; margin-bottom:8px; }
.kpi-card { border-radius:14px; padding:16px 14px 13px;
            font-family:"PingFang TC","PingFang SC",-apple-system,BlinkMacSystemFont,sans-serif;
            transition:transform .18s ease,box-shadow .18s ease; cursor:default; }
.kpi-card:hover { transform:translateY(-3px); box-shadow:0 8px 28px rgba(0,0,0,.12)!important; }
.kpi-lbl { font-size:14px; font-weight:700; color:#8B7355; margin-bottom:7px;
            display:flex; align-items:center; white-space:nowrap;
            overflow:hidden; text-overflow:ellipsis; }
.kpi-val { font-size:26px; font-weight:800; color:#374151; letter-spacing:-.02em;
            margin-bottom:7px; white-space:nowrap; }
.kpi-bdg { display:inline-block; font-size:12px; font-weight:600;
            border-radius:6px; padding:4px 8px; white-space:nowrap; }

/* ── Mobile ── */
@media (max-width: 768px) {
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebarCollapsedControl"] { display: none !important; }
    .main .block-container { padding: 0.5rem 0.75rem 2rem !important; }
    .sec-hd { font-size: 16px !important; margin: 12px 0 10px !important; }
    .stTabs [data-baseweb="tab"] { font-size: 14px !important; padding: 8px 16px !important; }
    /* Header banner */
    .main-hd { flex-direction: column !important; padding: 1rem !important;
                margin: 0 -0.75rem 1rem !important; gap: 10px !important; }
    .hd-logo  { height: 48px !important; width: 48px !important; }
    .hd-title { font-size: 1.25rem !important; line-height: 1.2 !important; }
    .hd-sub   { font-size: 11px !important; }
    .hd-note  { font-size: 11px !important; margin-top: 4px !important; }
    .hd-date  { text-align: left !important; margin-top: 0 !important; }
    .hd-date-main { font-size: 13px !important; font-weight: 600 !important; }
    .hd-date-vs   { font-size: 11px !important; }
    /* KPI cards 2-col on mobile */
    .kpi-grid { grid-template-columns: repeat(2,1fr) !important; gap:8px !important; }
    .kpi-card { padding:10px 10px 9px !important; border-radius:10px !important; }
    .kpi-lbl  { font-size:11px !important; margin-bottom:4px !important; }
    .kpi-val  { font-size:18px !important; margin-bottom:4px !important; }
    .kpi-bdg  { font-size:10px !important; padding:2px 6px !important; }
    /* GA4 orange banner */
    .ga4-hd { flex-direction: column !important; align-items: flex-start !important;
               padding: 14px 16px !important; gap: 6px !important; }
    .ga4-hd-title { font-size: 1.1rem !important; }
    .ga4-hd-date  { text-align: left !important; font-size: 12px !important; }
}
</style>""", unsafe_allow_html=True)

st.markdown("""<style>
[data-testid="stDataFrame"] thead tr th {
    background: #C8B99A !important;
    color: #2D1F0F !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    text-align: center !important;
}
[data-testid="stDataFrame"] tbody td {
    font-size: 16px !important;
    text-align: left !important;
}
</style>""", unsafe_allow_html=True)



try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30 * 60 * 1000, key="dash_refresh")
except ImportError:
    pass

# ─── PALETTE ──────────────────────────────────────────────────────────────────
BRAND_BLUE  = "#337AB7"
BRAND_RED   = "#F62B2B"
GA4_PRIMARY = "#E8710A"
GA4_AMBER   = "#F9AB00"
ROAS_TARGET = 3.0

REGION_ZH = {
    "Taichung City":    "台中市",   "Changhua County":  "彰化縣",
    "Taipei City":      "台北市",   "Taoyuan City":     "桃園市",
    "Kaohsiung City":   "高雄市",   "Hsinchu County":   "新竹縣",
    "Yunlin County":    "雲林縣",   "New Taipei City":  "新北市",
    "Nantou County":    "南投縣",   "Tainan City":      "台南市",
    "Hualien County":   "花蓮縣",   "Miaoli County":    "苗栗縣",
    "Chiayi City":      "嘉義市",   "Chiayi County":    "嘉義縣",
    "Pingtung County":  "屏東縣",   "Taitung County":   "台東縣",
    "Keelung City":     "基隆市",   "Hsinchu City":     "新竹市",
    "Yilan County":     "宜蘭縣",   "Penghu County":    "澎湖縣",
}

C = {
    "impressions": "#64748B", "reach":       "#475569",
    "freq":        "#F97316", "clicks":      "#0EA5E9",
    "ctr":         "#06B6D4", "cpc":         "#DB2777",
    "link_clicks": BRAND_BLUE,"link_ctr":    "#2563A8",
    "lpv":         "#7C3AED", "roas":        "#F59E0B",
    "purchases":   "#10B981", "revenue":     "#EC4899",
    "cpa":         BRAND_RED, "aov":         "#8B5CF6",
    "cvr":         "#059669", "cart":        "#EF4444",
    "checkout":    "#F97316", "atc_rate":    "#10B981",
    "checkout_rt": "#0EA5E9", "abandon":     "#DC2626",
    "cpa_cart":    "#BE185D", "cpm":         "#6D28D9",
}

FUNNEL_COLORS = [BRAND_BLUE, "#06B6D4", "#10B981", "#F59E0B", BRAND_RED]

PIE_COLORS = [
    "#1877F2", "#00B2D6", "#E8710A", "#F9AB00", "#34A853",
    "#EA4335", "#8B5CF6", "#EC4899", "#06B6D4", "#10B981",
    "#F59E0B", "#EF4444", "#6366F1", "#14B8A6", "#F97316",
]

CHART_BASE = dict(
    paper_bgcolor="#FFFDF8",
    plot_bgcolor="#FAF4EB",
    font=dict(
        family="PingFang TC,PingFang SC,-apple-system,BlinkMacSystemFont,sans-serif",
        size=12, color="#2D1F0F",
    ),
)

# ─── DATE RANGE HELPER ────────────────────────────────────────────────────────
def _compute_dates(key, custom_s=None, custom_u=None):
    """Return (s, u, cs, cu) as date objects for any preset key."""
    today = date.today()
    def _last_day(y, m):
        if m == 12: return date(y + 1, 1, 1) - timedelta(days=1)
        return date(y, m + 1, 1) - timedelta(days=1)
    def _dsun(d):   # days since last Sunday (Sun=0)
        return (d.weekday() + 1) % 7
    def _dmon(d):   # days since last Monday (Mon=0)
        return d.weekday()
    def _q_start(d):
        m = ((d.month - 1) // 3) * 3 + 1
        return date(d.year, m, 1)
    def _q_end(d):
        qs = _q_start(d)
        return _last_day(qs.year, qs.month + 2 if qs.month <= 10 else 12)

    if key == "今天":
        s = u = today
        cs = cu = today - timedelta(days=1)
    elif key == "昨天":
        s = u = today - timedelta(days=1)
        cs = cu = today - timedelta(days=2)
    elif key == "本週 (自星期日起)":
        s = today - timedelta(days=_dsun(today))
        u = s + timedelta(days=6)
        cs = s - timedelta(weeks=1); cu = u - timedelta(weeks=1)
    elif key == "本週至今 (自星期日起)":
        s = today - timedelta(days=_dsun(today))
        u = max(today - timedelta(days=1), s)
        n = (u - s).days
        cs = s - timedelta(weeks=1); cu = cs + timedelta(days=n)
    elif key == "本週 (自星期一起)":
        s = today - timedelta(days=_dmon(today))
        u = s + timedelta(days=6)
        cs = s - timedelta(weeks=1); cu = u - timedelta(weeks=1)
    elif key == "本週至今 (自星期一起)":
        s = today - timedelta(days=_dmon(today))
        u = max(today - timedelta(days=1), s)
        n = (u - s).days
        cs = s - timedelta(weeks=1); cu = cs + timedelta(days=n)
    elif key == "本月":
        s = today.replace(day=1)
        u = _last_day(today.year, today.month)
        cs = s - relativedelta(months=1); cu = _last_day(cs.year, cs.month)
    elif key in ("本月至今", "近 30 天 (預設)"):
        s = today.replace(day=1); u = today - timedelta(days=1)
        n = max((u - s).days, 0)
        cs = s - relativedelta(months=1); cu = cs + timedelta(days=n)
    elif key == "本季":
        s = _q_start(today); u = _q_end(today)
        cs = _q_start(today - relativedelta(months=3))
        cu = _q_end(today - relativedelta(months=3))
    elif key == "本季至今":
        s = _q_start(today); u = today - timedelta(days=1)
        n = max((u - s).days, 0)
        cs = _q_start(today - relativedelta(months=3))
        cu = cs + timedelta(days=n)
    elif key == "今年":
        s = date(today.year, 1, 1); u = date(today.year, 12, 31)
        cs = date(today.year - 1, 1, 1); cu = date(today.year - 1, 12, 31)
    elif key == "今年至今":
        s = date(today.year, 1, 1); u = today - timedelta(days=1)
        n = max((u - s).days, 0)
        cs = date(today.year - 1, 1, 1); cu = cs + timedelta(days=n)
    elif key in ("最近 7 天", "近 7 天"):
        u = today - timedelta(days=1); s = u - timedelta(days=6)
        cu = s - timedelta(days=1); cs = cu - timedelta(days=6)
    elif key == "過去 14 天":
        u = today - timedelta(days=1); s = u - timedelta(days=13)
        cu = s - timedelta(days=1); cs = cu - timedelta(days=13)
    elif key == "最近 28 天":
        u = today - timedelta(days=1); s = u - timedelta(days=27)
        cu = s - timedelta(days=1); cs = cu - timedelta(days=27)
    elif key in ("最近 30 天", "近 30 天"):
        u = today - timedelta(days=1); s = u - timedelta(days=29)
        cu = s - timedelta(days=1); cs = cu - timedelta(days=29)
    elif key == "上週 (自星期日起)":
        s = today - timedelta(days=_dsun(today) + 7)
        u = s + timedelta(days=6)
        cs = s - timedelta(weeks=1); cu = u - timedelta(weeks=1)
    elif key == "上週 (自星期一起)":
        s = today - timedelta(days=_dmon(today) + 7)
        u = s + timedelta(days=6)
        cs = s - timedelta(weeks=1); cu = u - timedelta(weeks=1)
    elif key in ("上個月", "上月"):
        first = today.replace(day=1)
        u = first - timedelta(days=1); s = u.replace(day=1)
        cu = s - timedelta(days=1); cs = cu.replace(day=1)
    elif key == "上一季":
        prev_q_end = _q_start(today) - timedelta(days=1)
        s = _q_start(prev_q_end); u = prev_q_end
        ppq_end = _q_start(s) - timedelta(days=1)
        cs = _q_start(ppq_end); cu = ppq_end
    elif key == "去年":
        s = date(today.year - 1, 1, 1); u = date(today.year - 1, 12, 31)
        cs = date(today.year - 2, 1, 1); cu = date(today.year - 2, 12, 31)
    elif key == "固定" and custom_s and custom_u:
        s, u = custom_s, custom_u
        n = max((u - s).days, 0)
        cu = s - timedelta(days=1); cs = cu - timedelta(days=n)
    else:  # 本月至今 (default)
        s = today.replace(day=1); u = today - timedelta(days=1)
        n = max((u - s).days, 0)
        cs = s - relativedelta(months=1); cu = cs + timedelta(days=n)
    return s, u, cs, cu

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def load_meta(since, until, cs, cu):
    from fetch_meta_tsaiyuan import get_meta_data_flex, summarize_flex, get_daily_data
    data    = get_meta_data_flex(since, until, cs, cu)
    summary = summarize_flex(data)
    daily   = get_daily_data(since=since, until=until)
    return summary, daily

@st.cache_data(ttl=1800, show_spinner=False)
def load_ga4(since, until, cs, cu):
    try:
        from fetch_ga4_data import get_ga4_data
        return get_ga4_data(since, until, cs, cu), None
    except Exception as e:
        return None, str(e)

def safe_pct(n, d):
    return round((1 - n / d) * 100, 1) if d > 0 else 0.0

def _chg_delta(curr, prev):
    if not prev:
        return None
    return round((curr - prev) / prev * 100, 1)

# ─── KPI CARD HTML ────────────────────────────────────────────────────────────
def kpi_html(cards, cols=7, card_bg="#FFFDF8"):
    divs = ""
    for c in cards:
        dv  = c.get("delta")
        inv = c.get("inverse", False)
        if c.get("spend_card"):
            arr  = "▲" if (dv or 0) > 0 else "▼"
            good = (dv or 0) > 0
            bdg_color = "#A7F3D0" if good else "#FCD34D"
            badge = (
                f'<span class="kpi-bdg" style="background:rgba(255,255,255,0.15);color:{bdg_color}">'
                f'{arr} {abs(dv or 0):.1f}% vs 上期</span>'
            ) if dv is not None else (
                '<span class="kpi-bdg" style="background:rgba(255,255,255,0.12);'
                'color:rgba(255,255,255,0.55)">— 無比較</span>'
            )
            divs += (
                f'<div class="kpi-card" style="border-top:none;'
                f'background:linear-gradient(135deg,#0369A1 0%,#0EA5E9 55%,#38BDF8 100%);'
                f'box-shadow:0 4px 20px rgba(3,105,161,.35)">'
                f'<div class="kpi-lbl" style="color:rgba(255,255,255,.75)">'
                f'<span style="display:inline-block;width:6px;height:6px;border-radius:50%;'
                f'background:rgba(255,255,255,.6);margin-right:5px;vertical-align:middle;flex-shrink:0"></span>'
                f'{c["label"]}</div>'
                f'<div class="kpi-val" style="color:#fff">{c["value"]}</div>'
                f'{badge}</div>'
            )
            continue
        if dv is not None:
            good  = (dv < 0) if inv else (dv > 0)
            dc    = "#059669" if good else "#DC2626"
            arr   = "▲" if dv > 0 else "▼"
            badge = f'<span class="kpi-bdg" style="background:{dc}18;color:{dc}">{arr} {abs(dv):.1f}% vs 上期</span>'
        else:
            badge = '<span class="kpi-bdg" style="background:#F0E5D018;color:#8B7355">— 無比較</span>'
        col = c.get("color", BRAND_BLUE)
        divs += (
            f'<div class="kpi-card" style="border-top:3px solid {col};background:{card_bg};'
            f'box-shadow:0 0 20px {col}28,0 2px 8px rgba(0,0,0,.05)">'
            f'<div class="kpi-lbl">'
            f'<span style="display:inline-block;width:6px;height:6px;border-radius:50%;'
            f'background:{col};margin-right:5px;vertical-align:middle;flex-shrink:0"></span>'
            f'{c["label"]}</div>'
            f'<div class="kpi-val">{c["value"]}</div>'
            f'{badge}</div>'
        )
    return (
        f'<div class="kpi-grid" style="grid-template-columns:repeat({cols},1fr)">'
        f'{divs}</div>'
    )

# ─── SPEND MINI CARD (lighter sky blue) ──────────────────────────────────────
# ─── FUNNEL HTML ──────────────────────────────────────────────────────────────
def funnel_html(stages):
    max_val = stages[0]["value"] if stages else 1
    body = ""
    for i, s in enumerate(stages):
        v  = s["value"]
        pv = s.get("prev_value", 0)
        w  = max(10, int(math.log(v + 1) / math.log(max_val + 1) * 100)) if max_val > 0 and v > 0 else 10
        # vs 上期比較
        if pv > 0:
            chg = (v - pv) / pv * 100
            arr = "▲" if chg > 0 else "▼"
            chg_color = "#059669" if chg > 0 else "#DC2626"
            cmp_html = f'<span style="color:{chg_color};font-size:11px;font-weight:700">{arr} {abs(chg):.1f}% vs 上期</span>'
        else:
            cmp_html = '<span style="color:#9CA3AF;font-size:11px">—</span>'
        # Stage bar row
        body += (
            f'<div class="row">'
            f'<div class="bw" style="width:{w}%;min-width:110px">'
            f'<div class="bar" style="background:linear-gradient(135deg,{s["color"]}EE 0%,{s["color"]} 100%)">'
            f'<span class="nm">{s["name"]}</span>'
            f'<span class="ct">{v:,}</span>'
            f'</div></div>'
            f'<div class="meta">{cmp_html}</div>'
            f'</div>'
        )
        # Connector between stages
        if i < len(stages) - 1:
            nxt = stages[i + 1]["value"]
            if v > 0:
                pass_n    = nxt
                loss_n    = v - nxt
                pass_pct  = nxt / v * 100
                loss_pct  = loss_n / v * 100
                next_color = stages[i + 1]["color"]
                body += (
                    f'<div class="conn">'
                    f'<span class="arr">↓</span>'
                    f'<span class="kept" style="color:{next_color}">'
                    f'繼續 {pass_pct:.1f}%（{pass_n:,} 人）</span>'
                    f'<span class="lost">流失 {loss_pct:.1f}%（{loss_n:,} 人）</span>'
                    f'</div>'
                )
            else:
                body += '<div class="conn"><span class="arr">↓</span><span class="lost">無資料</span></div>'
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:transparent;font-family:"PingFang TC","PingFang SC",-apple-system,sans-serif;padding:4px 0}}
.row{{display:flex;align-items:center;margin:0}}
.bw{{transition:width .4s ease}}
.bar{{height:46px;border-radius:10px;display:flex;align-items:center;
     justify-content:space-between;padding:0 14px;
     box-shadow:0 3px 12px rgba(0,0,0,.15),inset 0 1px 0 rgba(255,255,255,.15)}}
.nm{{color:rgba(255,255,255,.88);font-size:10px;font-weight:700;
     text-transform:uppercase;letter-spacing:.06em;flex-shrink:0}}
.ct{{color:#fff;font-size:20px;font-weight:900;margin-left:8px;white-space:nowrap;
     text-shadow:0 1px 3px rgba(0,0,0,.2)}}
.meta{{display:flex;align-items:center;padding-left:12px;min-width:140px}}
.conn{{display:flex;align-items:center;gap:10px;padding:3px 0 3px 22px;min-height:28px}}
.arr{{color:#C8B99A;font-size:13px;width:18px;flex-shrink:0}}
.kept{{font-size:11px;font-weight:700}}
.lost{{font-size:11px;font-weight:600;color:#9CA3AF}}
</style></head><body>{body}</body></html>"""

# ─── ROAS INSIGHTS（無表情符號、無**） ───────────────────────────────────────
def roas_insights(df, target=ROAS_TARGET):
    if df.empty or len(df) < 2:
        return []
    dv = df[df["roas"] > 0].copy()
    if dv.empty:
        return []
    dv["weekday"] = dv["date"].dt.weekday
    day_names = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    lines = []

    peak     = dv.loc[dv["roas"].idxmax()]
    pk_dt    = peak["date"].strftime("%m/%d")
    pk_val   = peak["roas"]
    pk_day   = day_names[int(peak["weekday"])]
    lines.append(f"最高 ROAS {pk_val:.2f}，出現在 {pk_dt}（{pk_day}）")

    above = dv[dv["roas"] >= target].copy()
    if not above.empty:
        dates_list = above["date"].dt.strftime("%m/%d").tolist()
        if len(dates_list) <= 6:
            dates_str = "、".join(dates_list)
        else:
            dates_str = "、".join(dates_list[:5]) + f"… 等共 {len(dates_list)} 天"
        lines.append(f"共 {len(dates_list)} 天 ROAS 超過目標 {target:.1f}，分別是：{dates_str}")
        wd = int((above["weekday"] < 5).sum())
        we = int((above["weekday"] >= 5).sum())
        if wd > 0 and we > 0:
            lines.append(
                f"超標日中：平日 {wd} 天、假日 {we} 天，"
                + ("平日轉換更穩定，建議維持平日預算" if wd > we else "假日轉換效率更高，可考慮假日加碼")
            )
        elif wd > 0:
            lines.append(f"超標日全在平日（{wd} 天），週末可嘗試調整出價或素材策略")
        else:
            lines.append(f"超標日全在假日（{we} 天），平日轉換偏低，建議優化平日素材")
    else:
        lines.append(f"本期尚無任何一天 ROAS 達到目標 {target:.1f}，全期均需優化")

    r7 = dv.tail(7)["roas"].mean()
    lines.append(f"近 7 日平均 ROAS：{r7:.2f}")

    if len(dv) >= 14:
        p7 = dv.iloc[-14:-7]["roas"].mean()
        diff = r7 - p7
        if r7 > p7 * 1.05:
            lines.append(
                f"趨勢上升：近 7 日（{r7:.2f}）比前 7 日（{p7:.2f}）高出 +{diff:.2f}，素材或受眾效果持續發酵"
            )
        elif r7 < p7 * 0.95:
            lines.append(
                f"趨勢下行：近 7 日（{r7:.2f}）低於前 7 日（{p7:.2f}）{abs(diff):.2f}，建議檢視素材是否疲勞"
            )
        else:
            lines.append(f"趨勢持平：近 7 日（{r7:.2f}）與前 7 日（{p7:.2f}）相近")

    weekday_avg = dv.groupby("weekday")["roas"].mean()
    if len(weekday_avg) > 0:
        best_day  = int(weekday_avg.idxmax())
        worst_day = int(weekday_avg.idxmin())
        lines.append(
            f"{day_names[best_day]} 平均 ROAS 最高（{weekday_avg[best_day]:.2f}），"
            f"{day_names[worst_day]} 最低（{weekday_avg[worst_day]:.2f}），"
            f"可調整預算分配提升整體效率"
        )
    return lines

def safe_pct(n, d):
    return round((1 - n / d) * 100, 1) if d > 0 else 0.0

def _chg_delta(curr, prev):
    if not prev:
        return None
    return round((curr - prev) / prev * 100, 1)

# ══════════════════════════════════════════════════════════════════════════════
# DATE RANGE SELECTOR — Looker Studio 風格（自製 HTML 日曆 v2）
# ══════════════════════════════════════════════════════════════════════════════
# 1. 讀取 query params（由 JS 套用後的 URL 傳入）
_qp = st.query_params.to_dict()
if "dp_since" in _qp:
    try:
        _qs = _qp["dp_since"]; _qu = _qp["dp_until"]
        date.fromisoformat(_qs); date.fromisoformat(_qu)
        st.session_state["since"] = _qs
        st.session_state["until"] = _qu
        _cs = _qp.get("dp_cs", ""); _cu = _qp.get("dp_cu", "")
        if not _cs or not _cu:
            _sd = date.fromisoformat(_qs); _ud = date.fromisoformat(_qu)
            _ndays = (_ud - _sd).days
            _cu_d = _sd - timedelta(days=1)
            _cs_d = _cu_d - timedelta(days=_ndays)
            _cs = _cs_d.strftime("%Y-%m-%d"); _cu = _cu_d.strftime("%Y-%m-%d")
        st.session_state["compare_since"] = _cs
        st.session_state["compare_until"] = _cu
        st.query_params.clear()
    except Exception:
        pass
    st.rerun()

# 2. 初始化 session_state 日期
if "since" not in st.session_state:
    _s0, _u0, _cs0, _cu0 = _compute_dates("本月至今")
    st.session_state["since"]         = _s0.strftime("%Y-%m-%d")
    st.session_state["until"]         = _u0.strftime("%Y-%m-%d")
    st.session_state["compare_since"] = _cs0.strftime("%Y-%m-%d")
    st.session_state["compare_until"] = _cu0.strftime("%Y-%m-%d")

since         = st.session_state["since"]
until         = st.session_state["until"]
compare_since = st.session_state["compare_since"]
compare_until = st.session_state["compare_until"]

def _dlbl(s):
    d = date.fromisoformat(s)
    return f"{d.year}年{d.month}月{d.day}日"

# 3. 日期選擇器 HTML 元件（v3：DOM-building，徹底修復點擊 + 放大20%）
_since_lbl = _dlbl(since)
_until_lbl = _dlbl(until)
_dp_html  = """<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:'PingFang TC','Microsoft JhengHei',sans-serif}
body{background:transparent;overflow:visible}
#dp-btn{display:inline-flex;align-items:center;gap:10px;padding:9px 18px;background:#fff;
  border:1.5px solid #C8B99A;border-radius:8px;cursor:pointer;font-size:15px;color:#2D1F0F;
  font-weight:600;white-space:nowrap;height:46px;justify-content:space-between;
  width:100%;max-width:380px;
  box-shadow:0 1px 4px rgba(0,0,0,.08);}
#dp-btn:hover{background:#FAF4EB;border-color:#A08060}
@media(max-width:900px){#dp-btn{max-width:100%;}}
</style></head><body>
<div id='dp-btn'>
  <span>&#128197;</span>
  <span id='dp-lbl'>SINCE_LBL &#9472; UNTIL_LBL</span>
  <span style='font-size:11px;opacity:.5'>&#9660;</span>
</div>
<script>
var SINCE='SINCE_VAL',UNTIL='UNTIL_VAL',CS='CS_VAL',CU='CU_VAL';
var selS=SINCE,selE=UNTIL,selCS=CS,selCU=CU;
var calSY=0,calSM=0,calEY=0,calEM=0,waitEnd=false;
function fmt(d){var y=d.getFullYear(),m=('0'+(d.getMonth()+1)).slice(-2),dd=('0'+d.getDate()).slice(-2);return y+'-'+m+'-'+dd;}
function addDays(d,n){var r=new Date(d);r.setDate(r.getDate()+n);return r;}
function dSun(d){return d.getDay();}
function dMon(d){return d.getDay()===0?6:d.getDay()-1;}
function computePreset(k){
  var t=new Date();t.setHours(0,0,0,0);var s,u,cs,cu,days;
  if(k==='今天'){s=u=t;cs=cu=addDays(t,-1);}
  else if(k==='昨天'){s=u=addDays(t,-1);cs=cu=addDays(t,-2);}
  else if(k==='本月至今'){s=new Date(t.getFullYear(),t.getMonth(),1);u=addDays(t,-1);days=Math.round((u-s)/864e5);cu=addDays(s,-1);cs=addDays(cu,-days);}
  else if(k==='本季至今'){var qm=[0,3,6,9],qs=qm.filter(function(m){return m<=t.getMonth();}).pop();s=new Date(t.getFullYear(),qs,1);u=addDays(t,-1);days=Math.round((u-s)/864e5);cu=addDays(s,-1);cs=addDays(cu,-days);}
  else if(k==='今年至今'){s=new Date(t.getFullYear(),0,1);u=addDays(t,-1);days=Math.round((u-s)/864e5);cu=addDays(s,-1);cs=addDays(cu,-days);}
  else if(k==='最近 7 天'){u=addDays(t,-1);s=addDays(u,-6);cu=addDays(s,-1);cs=addDays(cu,-6);}
  else if(k==='過去 14 天'){u=addDays(t,-1);s=addDays(u,-13);cu=addDays(s,-1);cs=addDays(cu,-13);}
  else if(k==='最近 28 天'){u=addDays(t,-1);s=addDays(u,-27);cu=addDays(s,-1);cs=addDays(cu,-27);}
  else if(k==='最近 30 天'){u=addDays(t,-1);s=addDays(u,-29);cu=addDays(s,-1);cs=addDays(cu,-29);}
  else if(k==='本週 (自星期日起)'){s=addDays(t,-dSun(t));u=addDays(s,6);cu=addDays(s,-1);cs=addDays(cu,-6);}
  else if(k==='本週至今 (自星期日起)'){s=addDays(t,-dSun(t));u=addDays(t,-1);days=Math.round((u-s)/864e5);cu=addDays(s,-1);cs=addDays(cu,-days);}
  else if(k==='本週 (自星期一起)'){s=addDays(t,-dMon(t));u=addDays(s,6);cu=addDays(s,-1);cs=addDays(cu,-6);}
  else if(k==='本週至今 (自星期一起)'){s=addDays(t,-dMon(t));u=addDays(t,-1);days=Math.round((u-s)/864e5);cu=addDays(s,-1);cs=addDays(cu,-days);}
  else if(k==='上週 (自星期日起)'){s=addDays(t,-dSun(t)-7);u=addDays(s,6);cu=addDays(s,-1);cs=addDays(cu,-6);}
  else if(k==='上週 (自星期一起)'){s=addDays(t,-dMon(t)-7);u=addDays(s,6);cu=addDays(s,-1);cs=addDays(cu,-6);}
  else if(k==='本月'){s=new Date(t.getFullYear(),t.getMonth(),1);u=new Date(t.getFullYear(),t.getMonth()+1,0);cu=addDays(s,-1);days=Math.round((u-s)/864e5);cs=addDays(cu,-days);}
  else if(k==='上個月'){var pm=t.getMonth()===0?12:t.getMonth(),py=t.getMonth()===0?t.getFullYear()-1:t.getFullYear();s=new Date(py,pm-1,1);u=new Date(py,pm,0);var ppm=pm===1?12:pm-1,ppy=pm===1?py-1:py;cs=new Date(ppy,ppm-1,1);cu=new Date(ppy,ppm,0);}
  else if(k==='本季'){var qm=[0,3,6,9],qs=qm.filter(function(m){return m<=t.getMonth();}).pop();s=new Date(t.getFullYear(),qs,1);u=new Date(t.getFullYear(),qs+3,0);cu=addDays(s,-1);days=Math.round((u-s)/864e5);cs=addDays(cu,-days);}
  else if(k==='上一季'){var qm=[0,3,6,9],qs=qm.filter(function(m){return m<=t.getMonth();}).pop();var pqs=qs===0?9:qs-3,pqy=qs===0?t.getFullYear()-1:t.getFullYear();s=new Date(pqy,pqs,1);u=new Date(pqy,pqs+3,0);cu=addDays(s,-1);days=Math.round((u-s)/864e5);cs=addDays(cu,-days);}
  else if(k==='今年'){s=new Date(t.getFullYear(),0,1);u=new Date(t.getFullYear(),11,31);cu=addDays(s,-1);days=Math.round((u-s)/864e5);cs=addDays(cu,-days);}
  else if(k==='去年'){s=new Date(t.getFullYear()-1,0,1);u=new Date(t.getFullYear()-1,11,31);cu=addDays(s,-1);days=Math.round((u-s)/864e5);cs=addDays(cu,-days);}
  else return null;
  return {s:fmt(s),u:fmt(u),cs:fmt(cs),cu:fmt(cu)};
}
/* Build calendar via DOM (no innerHTML + quotes conflict) */
function calGrid(doc,year,month,ss,se){
  var grid=doc.createElement('div');
  grid.style.cssText='display:grid;grid-template-columns:repeat(7,40px);gap:3px;margin-top:6px';
  ['日','一','二','三','四','五','六'].forEach(function(d){
    var h=doc.createElement('div');
    h.style.cssText='text-align:center;font-size:13px;color:#8B7355;padding:5px 0;font-weight:600';
    h.textContent=d;grid.appendChild(h);
  });
  var fd=new Date(year,month-1,1).getDay();
  for(var i=0;i<fd;i++) grid.appendChild(doc.createElement('div'));
  var dim=new Date(year,month,0).getDate();
  for(var d=1;d<=dim;d++){
    var ds=year+'-'+('0'+month).slice(-2)+'-'+('0'+d).slice(-2);
    var cell=doc.createElement('div');
    var isSel=(ds===ss||ds===se);
    var isRng=(ss&&se&&ds>ss&&ds<se);
    cell.style.cssText='text-align:center;padding:8px 0;font-size:14px;cursor:pointer;border-radius:'+(isSel?'50%':'5px')+
      ';color:'+(isSel?'#fff':'#2D1F0F')+';background:'+(isSel?'#337AB7':isRng?'#EBF3FB':'transparent')+
      ';font-weight:'+(isSel?'700':'400')+';user-select:none';
    cell.dataset.date=ds;
    cell.textContent=d;
    cell.addEventListener('mouseover',function(){if(!this.dataset.sel)this.style.background='#F0E5D0';});
    cell.addEventListener('mouseout',function(){if(!this.dataset.sel)this.style.background=this.dataset.bg||'transparent';});
    cell.dataset.bg=isSel?'#337AB7':isRng?'#EBF3FB':'transparent';
    cell.dataset.sel=isSel?'1':'';
    grid.appendChild(cell);
  }
  return grid;
}
function renderCals(){
  var p=window.parent.document.getElementById('ts-dp-panel');if(!p) return;
  var doc=window.parent.document;
  var sw=p.querySelector('#cal-s-wrap'),ew=p.querySelector('#cal-e-wrap');
  var sttl=p.querySelector('#cal-s-ttl'),ettl=p.querySelector('#cal-e-ttl');
  var pv=p.querySelector('#dp-pv'),co=p.querySelector('#dp-co');
  if(sw){sw.innerHTML='';sw.appendChild(calGrid(doc,calSY,calSM,selS,selE));}
  if(ew){ew.innerHTML='';ew.appendChild(calGrid(doc,calEY,calEM,selS,selE));}
  if(sttl) sttl.textContent=calSY+'年'+calSM+'月';
  if(ettl) ettl.textContent=calEY+'年'+calEM+'月';
  if(pv) pv.textContent=(selS||'—')+' → '+(selE||'點選結束日期');
  if(co) co.textContent='比較期：'+selCS+' ─ '+selCU;
}
function clickDate(ds){
  if(!waitEnd){selS=ds;selE='';waitEnd=true;}
  else{if(ds<selS){var t=selS;selS=ds;selE=t;}else selE=ds;
    waitEnd=false;
    var days=Math.round((new Date(selE)-new Date(selS))/864e5);
    var cud=new Date(selS);cud.setDate(cud.getDate()-1);
    var csd=new Date(cud);csd.setDate(csd.getDate()-days);
    selCS=fmt(csd);selCU=fmt(cud);
  }
  renderCals();
}
function applyPreset(k){
  if(!k) return;var r=computePreset(k);if(!r) return;
  selS=r.s;selE=r.u;selCS=r.cs;selCU=r.cu;waitEnd=false;
  var sd=new Date(selS),ed=new Date(selE);
  calSY=sd.getFullYear();calSM=sd.getMonth()+1;
  calEY=ed.getFullYear();calEM=ed.getMonth()+1;
  if(calEY===calSY&&calEM===calSM){calEM++;if(calEM>12){calEM=1;calEY++;}}
  renderCals();
}
function navCal(side,delta){
  if(side==='s'){calSM+=delta;if(calSM>12){calSM=1;calSY++;}if(calSM<1){calSM=12;calSY--;}}
  else{calEM+=delta;if(calEM>12){calEM=1;calEY++;}if(calEM<1){calEM=12;calEY--;}}
  renderCals();
}
function doApply(){
  if(!selS||!selE){alert('請先選擇完整日期範圍');return;}
  removePicker();
  /* Create form in PARENT document (not sandboxed) — sandbox restriction bypassed */
  var pdoc=window.parent.document;
  var f=pdoc.createElement('form');f.method='GET';f.action=window.parent.location.pathname||'/';
  var fields=[['dp_since',selS],['dp_until',selE],['dp_cs',selCS],['dp_cu',selCU]];
  fields.forEach(function(kv){var i=pdoc.createElement('input');i.type='hidden';i.name=kv[0];i.value=kv[1];f.appendChild(i);});
  pdoc.body.appendChild(f);f.submit();
}
function doCancel(){removePicker();}
function removePicker(){
  var p=window.parent.document.getElementById('ts-dp-panel');if(p) p.remove();
  var s=window.parent.document.getElementById('ts-dp-css');if(s) s.remove();
}
document.getElementById('dp-btn').addEventListener('click',function(){
  if(window.parent.document.getElementById('ts-dp-panel')){removePicker();return;}
  var iframe=window.frameElement;
  var rect=iframe.getBoundingClientRect();
  var sY=window.parent.scrollY||0,sX=window.parent.scrollX||0;
  var sd=new Date(SINCE),ed=new Date(UNTIL);
  calSY=sd.getFullYear();calSM=sd.getMonth()+1;
  calEY=ed.getFullYear();calEM=ed.getMonth()+1;
  if(calEY===calSY&&calEM===calSM){calEM++;if(calEM>12){calEM=1;calEY++;}}
  selS=SINCE;selE=UNTIL;selCS=CS;selCU=CU;waitEnd=false;
  var doc=window.parent.document;
  /* inject CSS */
  if(!doc.getElementById('ts-dp-css')){
    var style=doc.createElement('style');style.id='ts-dp-css';
    style.textContent='.cal-nav{background:none;border:1px solid #DDD0B8;border-radius:5px;padding:3px 12px;cursor:pointer;font-size:18px;color:#2D1F0F;line-height:1}.cal-nav:hover{background:#F0E5D0}';
    doc.head.appendChild(style);
  }
  /* build panel using DOM */
  var panel=doc.createElement('div');
  panel.id='ts-dp-panel';
  panel.style.cssText='position:absolute;top:'+(rect.bottom+sY+6)+'px;left:'+(rect.left+sX)+'px;background:#fff;border:1.5px solid #C8B99A;border-radius:14px;box-shadow:0 10px 36px rgba(0,0,0,.2);z-index:99999;padding:20px 22px;min-width:720px;font-family:PingFang TC,Microsoft JhengHei,sans-serif';
  /* === Looker Studio style hierarchical preset dropdown === */
  var preRow=doc.createElement('div');preRow.style.cssText='display:flex;justify-content:flex-end;margin-bottom:14px;position:relative';
  var presetLbl='自動日期範圍';
  var preBtn=doc.createElement('div');preBtn.id='dp-preset-btn';
  preBtn.style.cssText='border:1px solid #C8B99A;border-radius:7px;padding:7px 16px;font-size:14px;background:#FAF4EB;color:#2D1F0F;cursor:pointer;min-width:185px;display:flex;justify-content:space-between;align-items:center;user-select:none;gap:8px';
  var preTxt=doc.createElement('span');preTxt.id='dp-preset-lbl';preTxt.textContent=presetLbl;
  var preArr=doc.createElement('span');preArr.textContent='\u25be';preArr.style.cssText='font-size:11px;opacity:.5';
  preBtn.appendChild(preTxt);preBtn.appendChild(preArr);preRow.appendChild(preBtn);panel.appendChild(preRow);
  /* menu data */
  var MDATA=[
    {label:'\u56fa\u5b9a',fixed:true},
    {label:'\u4eca\u5929',key:'\u4eca\u5929'},
    {label:'\u6628\u5929',key:'\u6628\u5929'},
    {label:'\u672c\u6708',children:['\u672c\u9031 (\u81ea\u661f\u671f\u65e5\u8d77)','\u672c\u9031\u81f3\u4eca (\u81ea\u661f\u671f\u65e5\u8d77)','\u672c\u9031 (\u81ea\u661f\u671f\u4e00\u8d77)','\u672c\u9031\u81f3\u4eca (\u81ea\u661f\u671f\u4e00\u8d77)','\u672c\u6708','\u672c\u6708\u81f3\u4eca','\u672c\u5b63','\u672c\u5b63\u81f3\u4eca','\u4eca\u5e74','\u4eca\u5e74\u81f3\u4eca']},
    {label:'\u6700\u8fd1 7 \u5929',children:['\u6700\u8fd1 7 \u5929','\u904e\u53bb 14 \u5929','\u6700\u8fd1 28 \u5929','\u6700\u8fd1 30 \u5929','\u4e0a\u9031 (\u81ea\u661f\u671f\u65e5\u8d77)','\u4e0a\u9031 (\u81ea\u661f\u671f\u4e00\u8d77)','\u4e0a\u500b\u6708','\u4e0a\u4e00\u5b63','\u53bb\u5e74']},
  ];
  var dropMenu=doc.createElement('div');dropMenu.id='dp-drop';
  dropMenu.style.cssText='display:none;position:absolute;top:100%;right:0;background:#fff;border:1px solid #E0D5C5;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,.18);z-index:100001;min-width:200px;padding:4px 0;margin-top:4px';
  function pickPreset(key,label){
    presetLbl=label;var lbl=doc.getElementById('dp-preset-lbl');if(lbl)lbl.textContent=label;
    dropMenu.style.display='none';if(key)applyPreset(key);
  }
  var allSubs=[];
  MDATA.forEach(function(item){
    var li=doc.createElement('div');
    li.style.cssText='position:relative;padding:9px 16px;cursor:pointer;font-size:14px;color:#2D1F0F;display:flex;justify-content:space-between;align-items:center;white-space:nowrap';
    var lspan=doc.createElement('span');lspan.textContent=item.label;li.appendChild(lspan);
    if(item.children){
      var arr2=doc.createElement('span');arr2.textContent='\u25b6';arr2.style.cssText='font-size:10px;color:#8B7355;margin-left:20px';li.appendChild(arr2);
      var sub=doc.createElement('div');
      sub.style.cssText='display:none;position:absolute;left:100%;top:-4px;background:#fff;border:1px solid #E0D5C5;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,.18);min-width:200px;padding:4px 0;z-index:100002';
      item.children.forEach(function(ch){
        var si=doc.createElement('div');si.style.cssText='padding:9px 16px;cursor:pointer;font-size:14px;color:#2D1F0F;white-space:nowrap';si.textContent=ch;
        si.addEventListener('mouseover',function(){this.style.background='#FAF4EB';});
        si.addEventListener('mouseout',function(){this.style.background='';});
        si.addEventListener('click',function(e){e.stopPropagation();pickPreset(ch,ch);});
        sub.appendChild(si);
      });
      li.appendChild(sub);allSubs.push(sub);
      var ht2=null;
      li.addEventListener('mouseenter',function(){allSubs.forEach(function(s){s.style.display='none';});sub.style.display='block';if(ht2){clearTimeout(ht2);ht2=null;}});
      li.addEventListener('mouseleave',function(){ht2=setTimeout(function(){sub.style.display='none';},120);});
      sub.addEventListener('mouseenter',function(){if(ht2){clearTimeout(ht2);ht2=null;}});
      sub.addEventListener('mouseleave',function(){ht2=setTimeout(function(){sub.style.display='none';},120);});
    } else {
      li.addEventListener('mouseenter',function(){allSubs.forEach(function(s){s.style.display='none';});});
      li.addEventListener('click',function(e){e.stopPropagation();if(!item.fixed)pickPreset(item.key,item.label);else dropMenu.style.display='none';});
    }
    li.addEventListener('mouseover',function(){this.style.background='#FAF4EB';});
    li.addEventListener('mouseout',function(){this.style.background='';});
    dropMenu.appendChild(li);
  });
  preRow.appendChild(dropMenu);
  preBtn.addEventListener('click',function(e){e.stopPropagation();dropMenu.style.display=dropMenu.style.display==='block'?'none':'block';});
  panel.addEventListener('click',function(e){var dd=doc.getElementById('dp-drop');if(dd&&!preBtn.contains(e.target)&&!dd.contains(e.target))dd.style.display='none';});
  /* preview */
  var pv=doc.createElement('div');pv.id='dp-pv';
  pv.style.cssText='font-size:14px;color:#374151;font-weight:700;text-align:center;margin-bottom:12px';
  pv.textContent=SINCE+' → '+UNTIL;panel.appendChild(pv);
  /* calendars row */
  var calRow=doc.createElement('div');calRow.style.cssText='display:flex;gap:28px';
  function makeCalCol(side){
    var col=doc.createElement('div');col.style.flex='1';
    var hdr=doc.createElement('div');hdr.style.cssText='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px';
    var btnP=doc.createElement('button');btnP.className='cal-nav';btnP.id=side+'P';btnP.textContent='‹';
    var ttl=doc.createElement('span');ttl.id='cal-'+side+'-ttl';ttl.style.cssText='font-size:15px;font-weight:700;color:#2D1F0F';
    var btnN=doc.createElement('button');btnN.className='cal-nav';btnN.id=side+'N';btnN.textContent='›';
    hdr.appendChild(btnP);hdr.appendChild(ttl);hdr.appendChild(btnN);col.appendChild(hdr);
    var lbl=doc.createElement('div');lbl.style.cssText='font-size:12px;color:#8B7355;text-align:center;margin-bottom:6px;font-weight:600';
    lbl.textContent=side==='s'?'開始日期':'結束日期';col.appendChild(lbl);
    var wrap=doc.createElement('div');wrap.id='cal-'+side+'-wrap';col.appendChild(wrap);
    return col;
  }
  calRow.appendChild(makeCalCol('s'));calRow.appendChild(makeCalCol('e'));panel.appendChild(calRow);
  /* compare */
  var co=doc.createElement('div');co.id='dp-co';
  co.style.cssText='font-size:13px;color:#8B7355;margin-top:12px;text-align:right';
  co.textContent='比較期：'+CS+' ─ '+CU;panel.appendChild(co);
  /* footer buttons */
  var foot=doc.createElement('div');foot.style.cssText='display:flex;justify-content:flex-end;gap:12px;margin-top:16px;border-top:1px solid #F0E5D0;padding-top:14px';
  var btnC=doc.createElement('button');btnC.id='dp-cancel';
  btnC.style.cssText='padding:9px 26px;border:1.5px solid #C8B99A;background:#fff;border-radius:7px;cursor:pointer;font-size:15px;color:#4B3621;font-weight:600';
  btnC.textContent='取消';
  var btnA=doc.createElement('button');btnA.id='dp-apply';
  btnA.style.cssText='padding:9px 32px;background:#337AB7;color:#fff;border:none;border-radius:7px;cursor:pointer;font-size:15px;font-weight:700';
  btnA.textContent='套用';
  foot.appendChild(btnC);foot.appendChild(btnA);panel.appendChild(foot);
  doc.body.appendChild(panel);
  renderCals();
  /* event listeners (all from iframe scope — closures work cross-frame) */
  btnC.addEventListener('click',doCancel);
  btnA.addEventListener('click',doApply);
  doc.getElementById('sP').addEventListener('click',function(){navCal('s',-1);});
  doc.getElementById('sN').addEventListener('click',function(){navCal('s',1);});
  doc.getElementById('eP').addEventListener('click',function(){navCal('e',-1);});
  doc.getElementById('eN').addEventListener('click',function(){navCal('e',1);});
  /* delegation on wrapper divs — survives renderCals rebuild */
  panel.querySelector('#cal-s-wrap').addEventListener('click',function(e){
    if(e.target.dataset&&e.target.dataset.date) clickDate(e.target.dataset.date);});
  panel.querySelector('#cal-e-wrap').addEventListener('click',function(e){
    if(e.target.dataset&&e.target.dataset.date) clickDate(e.target.dataset.date);});
  /* close on outside click */
  setTimeout(function(){
    doc.addEventListener('click',function h(e){
      var p=doc.getElementById('ts-dp-panel');
      if(!p){doc.removeEventListener('click',h,true);return;}
      if(!p.contains(e.target)&&!iframe.contains(e.target)){
        removePicker();doc.removeEventListener('click',h,true);}
    },true);
  },150);
});
</script></body></html>"""
_dp_html = (_dp_html
    .replace('SINCE_LBL', _since_lbl)
    .replace('UNTIL_LBL', _until_lbl)
    .replace('SINCE_VAL', since)
    .replace('UNTIL_VAL', until)
    .replace('CS_VAL', compare_since)
    .replace('CU_VAL', compare_until)
)

# 4. 渲染：日曆選擇器
components.html(_dp_html, height=50, scrolling=False)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR（品牌資訊 + 刷新）
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
# MAIN HEADER — 灰色漸層 + 中文標題 + 品牌 Logo
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f'''
<div class="main-hd" style="background:linear-gradient(135deg,#4B5563 0%,#6B7280 50%,#9CA3AF 100%);
            padding:1.8rem 2.2rem 2rem;margin:0 -2rem 1.8rem;
            display:flex;align-items:center;gap:28px">
  <img class="hd-logo" src="data:image/webp;base64,{LOGO_B64}"
       style="height:80px;width:80px;object-fit:contain;border-radius:50%;
              background:#FFFDF8;padding:7px;flex-shrink:0;
              box-shadow:0 2px 12px rgba(0,0,0,.20)"/>
  <div style="flex:1;min-width:0">
    <div class="hd-sub" style="color:rgba(255,255,255,.75);font-size:13px;font-weight:700;
                text-transform:uppercase;letter-spacing:.12em;margin-bottom:7px">
      采姸服飾 · 廣告數據報表系統
    </div>
    <div class="hd-title" style="color:#fff;font-size:2rem;font-weight:900;letter-spacing:-.025em;line-height:1.1;
                text-shadow:0 1px 3px rgba(0,0,0,.20);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
      采姸服裝 Meta 廣告數據總覽
    </div>
    <div class="hd-note" style="color:rgba(255,255,255,.75);font-size:14px;margin-top:7px">
      Meta Marketing API v21.0 × Google Analytics 4 · 每 30 分鐘自動刷新
    </div>
  </div>
  <div class="hd-date" style="text-align:right;flex-shrink:0">
    <div class="hd-date-main" style="color:#fff;font-size:16px;font-weight:700">{since} ～ {until}</div>
    <div class="hd-date-vs" style="color:rgba(255,255,255,.7);font-size:13px;margin-top:4px">vs {compare_since} ～ {compare_until}</div>
  </div>
</div>
''', unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab_meta, tab_ga4 = st.tabs(["  Meta 廣告成效  ", "  GA4 網站流量  "])

# Logo injection via parent-frame JS (bypasses CSP on ::before content)
_META_B64 = META_LOGO_B64
_GA4_B64  = GA4_LOGO_B64
components.html(f"""
<script>
(function() {{
  var META = "{_META_B64}";
  var GA4  = "{_GA4_B64}";
  function inject() {{
    var doc = window.parent ? window.parent.document : document;
    var tabs = doc.querySelectorAll('[data-baseweb="tab"]');
    if (tabs.length >= 2) {{
      [0, 1].forEach(function(i) {{
        if (!tabs[i].querySelector('.tj-logo')) {{
          var img = doc.createElement('img');
          img.src = 'data:image/png;base64,' + (i === 0 ? META : GA4);
          img.style.cssText = 'width:20px;height:20px;margin-right:7px;vertical-align:middle;object-fit:contain;display:inline-block;flex-shrink:0';
          img.className = 'tj-logo';
          tabs[i].insertBefore(img, tabs[i].firstChild);
        }}
      }});
    }}
  }}
  var t = setInterval(inject, 400);
  setTimeout(function() {{ clearInterval(t); }}, 8000);
}})();
</script>
""", height=0)

# ══════════════════════════════════════════════════════════════════════════════
# META 頁
# ══════════════════════════════════════════════════════════════════════════════
with tab_meta:
    with st.spinner("📡 連接 Meta API..."):
        try:
            summary, daily = load_meta(since, until, compare_since, compare_until)
        except Exception as e:
            st.error(f"⚠️ Meta 資料載入失敗：{e}")
            st.info("請確認 config/meta_ads.json Token 是否有效（到期日：2026-06-19）")
            st.stop()

    tm  = summary["account"]
    cm  = summary.get("compare_account", {})
    ads = summary["ads"]

    if daily:
        df = pd.DataFrame(daily).fillna(0)
        df["date"] = pd.to_datetime(df["date"])
    else:
        df = pd.DataFrame()

    cart_ab     = safe_pct(tm["initiate_checkout"], tm["add_to_cart"])
    checkout_ab = safe_pct(tm["purchases"],          tm["initiate_checkout"])
    cm_cart_ab  = safe_pct(cm.get("initiate_checkout", 0), cm.get("add_to_cart", 0))
    cm_chk_ab   = safe_pct(cm.get("purchases", 0),          cm.get("initiate_checkout", 0))
    cart_ab_chg = _chg_delta(cart_ab, cm_cart_ab) if cm_cart_ab > 0 else None
    chk_ab_chg  = _chg_delta(checkout_ab, cm_chk_ab) if cm_chk_ab > 0 else None
    days_n = max((datetime.strptime(until, "%Y-%m-%d") - datetime.strptime(since, "%Y-%m-%d")).days, 1)

    # 連結點擊成本（Link CPC）計算 — spend 已含 1.25x 乘數
    _cpl = tm["spend"] / tm["link_clicks"] if tm.get("link_clicks", 0) > 0 else 0
    _cpl_prev = cm.get("spend", 0) / cm["link_clicks"] if cm.get("link_clicks", 0) > 0 else 0
    _cpl_chg = round((_cpl - _cpl_prev) / _cpl_prev * 100, 1) if _cpl_prev > 0 else None

    # 流量指標（第一排 6 項）
    st.markdown('<div class="sec-hd">流量指標</div>', unsafe_allow_html=True)
    st.markdown(kpi_html([
        dict(label="曝光數",        value=f"{tm['impressions']:,}",
             delta=tm.get("impressions_chg"),       color=C["impressions"]),
        dict(label="觸及人數",      value=f"{tm['reach']:,}",
             delta=tm.get("reach_chg"),             color=C["reach"]),
        dict(label="廣告頻率",      value=f"{tm['frequency']:.2f} 次",
             delta=tm.get("frequency_chg"),         color=C["freq"],      inverse=True),
        dict(label="千次曝光成本",   value=f"${tm['cpm']:.2f}",
             delta=tm.get("cpm_chg"),               color=C["cpm"],       inverse=True),
        dict(label="點擊數（全部）",value=f"{tm['clicks']:,}",
             delta=tm.get("clicks_chg"),            color=C["clicks"]),
        dict(label="點閱率",        value=f"{tm['ctr']:.2f}%",
             delta=tm.get("ctr_chg"),               color=C["ctr"]),
    ], cols=6), unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    # 流量指標（第二排 5 項 + 廣告花費藍卡）
    st.markdown(kpi_html([
        dict(label="點擊成本",      value=f"${tm['cpc']:.2f}",
             delta=tm.get("cpc_chg"),               color=C["cpc"],       inverse=True),
        dict(label="連結點擊數",    value=f"{tm['link_clicks']:,}",
             delta=tm.get("link_clicks_chg"),       color=C["link_clicks"]),
        dict(label="連結點閱率",    value=f"{tm['link_ctr']:.2f}%",
             delta=tm.get("link_ctr_chg"),          color=C["link_ctr"]),
        dict(label="頁面瀏覽次數",  value=f"{tm.get('landing_page_view', 0):,}",
             delta=tm.get("landing_page_view_chg"), color=C["lpv"]),
        dict(label="連結點擊成本",   value=f"${_cpl:.2f}",
             delta=_cpl_chg,                        color=C["cpc"],       inverse=True),
        dict(label="廣告花費",      value=f"${tm['spend']:,.0f}",
             delta=tm.get("spend_chg"),             spend_card=True),
    ], cols=6), unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # 轉換指標
    st.markdown('<div class="sec-hd">轉換指標</div>', unsafe_allow_html=True)
    st.markdown(kpi_html([
        dict(label="加入購物車",    value=f"{tm['add_to_cart']:,}",
             delta=tm.get("add_to_cart_chg"),       color=C["cart"]),
        dict(label="開始結帳",      value=f"{tm['initiate_checkout']:,}",
             delta=tm.get("initiate_checkout_chg"), color=C["checkout"]),
        dict(label="購買數",        value=f"{tm['purchases']:,}",
             delta=tm.get("purchases_chg"),         color=C["purchases"]),
        dict(label="ROAS",          value=f"{tm['roas']:.2f}",
             delta=tm.get("roas_chg"),              color=C["roas"]),
        dict(label="轉換率",        value=f"{tm['conversion_rate']:.2f}%",
             delta=tm.get("conversion_rate_chg"),   color=C["cvr"]),
        dict(label="購買金額",      value=f"${tm['purchase_value']:,.0f}",
             delta=tm.get("purchase_value_chg"),    color=C["revenue"]),
        dict(label="平均客單價",    value=f"${tm['avg_order_value']:,.0f}" if tm["avg_order_value"] > 0 else "—",
             delta=tm.get("avg_order_value_chg"),   color=C["aov"]),
        dict(label="每單成本 CPA",  value=f"${tm['cpa']:.2f}" if tm["cpa"] > 0 else "—",
             delta=tm.get("cpa_chg"),               color=C["cpa"],       inverse=True),
    ], cols=8), unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # 購物旅程效率
    st.markdown('<div class="sec-hd">購物旅程效率</div>', unsafe_allow_html=True)
    st.markdown(kpi_html([
        dict(label="加購率",        value=f"{tm['add_to_cart_rate']:.2f}%",
             delta=tm.get("add_to_cart_rate_chg"),  color=C["atc_rate"]),
        dict(label="加購成本",      value=f"${tm.get('cpa_cart', 0):.2f}" if tm.get("cpa_cart", 0) > 0 else "—",
             delta=tm.get("cpa_cart_chg"),          color=C["cpa_cart"],  inverse=True),
        dict(label="開始結帳率",    value=f"{tm.get('checkout_rate', 0):.2f}%",
             delta=tm.get("checkout_rate_chg"),     color=C["checkout_rt"]),
        dict(label="購物車放棄率",  value=f"{cart_ab:.1f}%",
             delta=cart_ab_chg,                     color=C["abandon"],   inverse=True),
        dict(label="結帳放棄率",    value=f"{checkout_ab:.1f}%",
             delta=chk_ab_chg,                      color=C["abandon"],   inverse=True),
    ], cols=5), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.divider()

    # 趨勢 + 漏斗
    col_t, col_f = st.columns([58, 42])
    with col_t:
        st.markdown(f'<div class="sec-hd">每日趨勢 — 花費 vs 購買金額（{since} ～ {until}）</div>', unsafe_allow_html=True)
        if not df.empty:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            # 週末底紋
            for dt in df["date"]:
                if dt.weekday() >= 5:
                    fig.add_vrect(
                        x0=dt - pd.Timedelta(hours=12),
                        x1=dt + pd.Timedelta(hours=12),
                        fillcolor="rgba(0,0,0,0.035)", line_width=0, layer="below",
                    )
            fig.add_trace(go.Bar(
                x=df["date"], y=df["spend"], name="每日花費",
                marker=dict(
                    color="#38BDF8", opacity=0.82,
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{x|%m/%d}</b>　花費 $%{y:,.0f}<extra></extra>",
            ), secondary_y=False)
            fig.add_trace(go.Scatter(
                x=df["date"], y=df["purchase_value"], name="購買金額",
                line=dict(color="#FF7A00", width=3, shape="spline"),
                mode="lines+markers",
                marker=dict(size=6, color="#FF7A00", line=dict(color="white", width=1.5)),
                fill="tozeroy", fillcolor="rgba(255,122,0,0.06)",
                hovertemplate="<b>%{x|%m/%d}</b>　購買金額 $%{y:,.0f}<extra></extra>",
            ), secondary_y=True)
            fig.update_yaxes(title_text="花費 ($)", secondary_y=False,
                             showgrid=True, gridcolor="#E5D8C4",
                             gridwidth=1, zeroline=False,
                             tickfont=dict(size=11))
            fig.update_yaxes(title_text="購買金額 ($)", secondary_y=True,
                             showgrid=False, zeroline=False, tickfont=dict(size=11))
            fig.update_xaxes(showgrid=False, tickfont=dict(size=11))
            fig.update_layout(
                height=320, hovermode="x unified",
                legend=dict(orientation="h", y=1.08, x=0, font=dict(size=12),
                            bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=65, t=5, b=0), **CHART_BASE,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("趨勢資料不足")

    with col_f:
        st.markdown('<div class="sec-hd">電商購買漏斗</div>', unsafe_allow_html=True)
        components.html(funnel_html([
            {"name": "連結點擊",  "value": tm["link_clicks"],
             "prev_value": cm.get("link_clicks", 0),        "color": FUNNEL_COLORS[0]},
            {"name": "落地頁瀏覽","value": tm.get("landing_page_view", 0),
             "prev_value": cm.get("landing_page_view", 0),  "color": FUNNEL_COLORS[1]},
            {"name": "加入購物車","value": tm["add_to_cart"],
             "prev_value": cm.get("add_to_cart", 0),        "color": FUNNEL_COLORS[2]},
            {"name": "開始結帳",  "value": tm["initiate_checkout"],
             "prev_value": cm.get("initiate_checkout", 0),  "color": FUNNEL_COLORS[3]},
            {"name": "完成購買",  "value": tm["purchases"],
             "prev_value": cm.get("purchases", 0),          "color": FUNNEL_COLORS[4]},
        ]), height=370, scrolling=False)

    st.divider()

    # ROAS 趨勢 + 洞察
    st.markdown(
        f'<div class="sec-hd">ROAS 每日趨勢（{since} ～ {until}）· 7 日均線 · 目標 {ROAS_TARGET}</div>',
        unsafe_allow_html=True
    )
    if not df.empty:
        df["roas_ma7"] = df["roas"].rolling(7, min_periods=1).mean()
        fig_r = go.Figure()
        # 週末底紋
        for dt in df["date"]:
            if dt.weekday() >= 5:
                fig_r.add_vrect(
                    x0=dt - pd.Timedelta(hours=12),
                    x1=dt + pd.Timedelta(hours=12),
                    fillcolor="rgba(0,0,0,0.035)", line_width=0, layer="below",
                )
        # 超標綠區（ROAS ≥ 目標）
        fig_r.add_hrect(
            y0=ROAS_TARGET, y1=max(df["roas"].max() * 1.1, ROAS_TARGET + 1),
            fillcolor="rgba(16,185,129,0.06)", line_width=0, layer="below",
        )
        fig_r.add_trace(go.Scatter(
            x=df["date"], y=df["roas"], name="每日 ROAS",
            line=dict(color="#F59E0B", width=2.5, shape="spline"),
            fill="tozeroy", fillcolor="rgba(245,158,11,0.09)",
            mode="lines+markers",
            marker=dict(size=5, color="#F59E0B", line=dict(color="white", width=1.5)),
            hovertemplate="<b>%{x|%m/%d}</b>　ROAS: %{y:.2f}<extra></extra>",
        ))
        fig_r.add_trace(go.Scatter(
            x=df["date"], y=df["roas_ma7"], name="7 日均線",
            line=dict(color="#6366F1", width=2, dash="dot", shape="spline"),
            mode="lines",
            hovertemplate="<b>%{x|%m/%d}</b>　7日均: %{y:.2f}<extra></extra>",
        ))
        fig_r.add_hline(
            y=ROAS_TARGET, line_dash="dash", line_color="#10B981", line_width=1.5,
            annotation_text=f" 目標 {ROAS_TARGET}",
            annotation_font_color="#10B981", annotation_position="right",
        )
        fig_r.update_layout(
            height=260, hovermode="x unified",
            legend=dict(orientation="h", y=1.1, x=0, bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=80, t=5, b=0),
            yaxis=dict(title="ROAS", showgrid=True, gridcolor="#E5D8C4",
                       gridwidth=1, zeroline=False, tickfont=dict(size=11)),
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            **CHART_BASE,
        )
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

        insights = roas_insights(df)
        if insights:
            items = "".join(f'<li style="margin-bottom:7px;line-height:1.7">{i}</li>' for i in insights)
            st.markdown(
                f'<div style="background:#FFF8F0;border:1px solid #FDDCB5;border-radius:14px;'
                f'padding:16px 20px;margin-top:4px">'
                f'<div style="font-size:14px;font-weight:800;color:{GA4_PRIMARY};'
                f'margin-bottom:10px">ROAS 洞察摘要</div>'
                f'<ul style="margin:0;padding-left:18px;font-size:13.5px;color:#3D2E1E">'
                f'{items}</ul></div>',
                unsafe_allow_html=True,
            )

    st.divider()

    # 素材排行：縣市圓餅 + 素材表格
    st.markdown('<div class="sec-hd">素材效益排行</div>', unsafe_allow_html=True)

    if ads:
        ads_s = sorted(ads, key=lambda x: x["roas"], reverse=True)
        ga4_for_meta, _ = load_ga4(since, until, compare_since, compare_until)
        regions = (ga4_for_meta or {}).get("regions", [])

        col_pie, col_tbl = st.columns([36, 64])

        with col_pie:
            st.markdown(
                '<div style="font-size:14px;font-weight:700;color:#2D1F0F;margin-bottom:8px">'
                '各縣市購買表現（GA4）</div>',
                unsafe_allow_html=True,
            )
            if regions:
                labels = [REGION_ZH.get(r["region"], r["region"]) for r in regions]
                values = [r["key_events"] for r in regions]
                total_ev = sum(values)
                # Pull the highest-value slice (not always index 0)
                max_idx = values.index(max(values))
                _pull = [0.0] * len(labels)
                _pull[max_idx] = 0.06
                # Custom text: city name + count (white, horizontal, centered)
                _pie_text = [f"{l}<br>{v:,}次" for l, v in zip(labels, values)]
                fig_pie = go.Figure(go.Pie(
                    labels=labels, values=values,
                    hole=0.52,
                    marker=dict(colors=PIE_COLORS[:len(labels)],
                                line=dict(color="#FAF4EB", width=3)),
                    text=_pie_text,
                    textinfo="text+percent",
                    textposition="inside",
                    insidetextorientation="horizontal",
                    textfont=dict(size=10, color="white",
                                  family="PingFang TC,sans-serif"),
                    pull=_pull,
                    hovertemplate="<b>%{label}</b><br>購買事件：%{value:,}<br>占比：%{percent}<extra></extra>",
                ))
                fig_pie.add_annotation(
                    text=f"<b>{total_ev}</b><br><span style='font-size:11px'>總購買事件</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=15, color="#2D1F0F",
                              family="PingFang TC,PingFang SC,-apple-system,sans-serif"),
                )
                fig_pie.update_layout(
                    height=370,
                    margin=dict(l=10, r=10, t=16, b=10),
                    legend=dict(
                        orientation="v", x=1.01, y=0.5,
                        font=dict(size=11), bgcolor="rgba(0,0,0,0)"
                    ),
                    showlegend=True,
                    **CHART_BASE,
                )
                st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("縣市資料不足（GA4 地理位置追蹤可能未啟用）")

        with col_tbl:
            st.markdown(
                '<div style="font-size:14px;font-weight:700;color:#2D1F0F;margin-bottom:8px">'
                '所有素材完整指標</div>',
                unsafe_allow_html=True,
            )
            # 計算總計（用原始數值）
            _t_imp  = sum(a["impressions"] for a in ads_s)
            _t_clk  = sum(a["clicks"] for a in ads_s)
            _t_lc   = sum(a["link_clicks"] for a in ads_s)
            _t_atc  = sum(a["add_to_cart"] for a in ads_s)
            _t_ic   = sum(a["initiate_checkout"] for a in ads_s)
            _t_pur  = sum(a["purchases"] for a in ads_s)
            _t_pv   = sum(a["purchase_value"] for a in ads_s)
            _t_sp   = sum(a["spend"] for a in ads_s)
            _t_lpv  = sum(a.get("landing_page_view", 0) for a in ads_s)
            _t_ctr  = round(_t_clk / _t_imp * 100, 2) if _t_imp > 0 else 0
            _t_cpc  = round(_t_sp / _t_clk, 2) if _t_clk > 0 else 0
            _t_lctr = round(_t_lc / _t_imp * 100, 2) if _t_imp > 0 else 0
            _t_atcr = round(_t_atc / _t_lpv * 100, 2) if _t_lpv > 0 else 0
            _t_roas = round(_t_pv / _t_sp, 2) if _t_sp > 0 else 0
            _t_cpa  = round(_t_sp / _t_pur, 2) if _t_pur > 0 else 0
            _t_aov  = round(_t_pv / _t_pur, 0) if _t_pur > 0 else 0
            _t_cvr  = round(_t_pur / _t_lpv * 100, 2) if _t_lpv > 0 else 0

            rows_ads = [{
                "素材名稱":   a["name"][:30],
                "曝光":       f"{a['impressions']:,}",
                "點擊":       f"{a['clicks']:,}",
                "點閱率":     f"{a['ctr']:.2f}%",
                "點擊成本":   f"${a['cpc']:.2f}",
                "連結點擊":   f"{a['link_clicks']:,}",
                "連結點擊率": f"{a['link_ctr']:.2f}%",
                "加購":       f"{a['add_to_cart']:,}",
                "加購率":     f"{a['add_to_cart_rate']:.2f}%",
                "結帳":       f"{a['initiate_checkout']:,}",
                "購買":       f"{a['purchases']:,}",
                "ROAS":       round(a["roas"], 2),
                "CPA":        f"${a['cpa']:.2f}" if a["cpa"] > 0 else "—",
                "客單價":     f"${a['avg_order_value']:,.0f}" if a["avg_order_value"] > 0 else "—",
                "轉換率":     f"{a['conversion_rate']:.2f}%",
                "花費":       f"${a['spend']:,.0f}",
            } for a in ads_s]
            rows_ads.append({
                "素材名稱":   "總計",
                "曝光":       f"{_t_imp:,}",
                "點擊":       f"{_t_clk:,}",
                "點閱率":     f"{_t_ctr:.2f}%",
                "點擊成本":   f"${_t_cpc:.2f}",
                "連結點擊":   f"{_t_lc:,}",
                "連結點擊率": f"{_t_lctr:.2f}%",
                "加購":       f"{_t_atc:,}",
                "加購率":     f"{_t_atcr:.2f}%",
                "結帳":       f"{_t_ic:,}",
                "購買":       f"{_t_pur:,}",
                "ROAS":       _t_roas,
                "CPA":        f"${_t_cpa:.2f}" if _t_pur > 0 else "—",
                "客單價":     f"${_t_aov:,.0f}" if _t_pur > 0 else "—",
                "轉換率":     f"{_t_cvr:.2f}%",
                "花費":       f"${_t_sp:,.0f}",
            })
            # 在素材列和總計列之間插入空白，把總計固定在最底部
            _ADS_ROW_H = 35   # 與 GA4 表格一致
            _ADS_HDR_H = 38
            _ADS_MIN_ROWS = 10
            _ads_empty_n = max(0, _ADS_MIN_ROWS - len(rows_ads))  # rows_ads 已含總計
            _blank_ad = {k: "" for k in rows_ads[0].keys()}
            _blank_ad["ROAS"] = 0.0  # ProgressColumn 需要數值
            # 把空白行插在資料和總計之間
            total_ad_row = rows_ads.pop()
            rows_ads += [_blank_ad] * _ads_empty_n + [total_ad_row]
            df_ads = pd.DataFrame(rows_ads)

            def _style_ads_total(df):
                def _rs(row):
                    if row.name == len(df) - 1:
                        return [f'background-color:#EDE8DF;font-weight:700;color:#2D1F0F'] * len(row)
                    return [''] * len(row)
                return df.style.apply(_rs, axis=1)

            roas_max = max((a["roas"] for a in ads_s), default=1) + 0.5
            st.dataframe(
                _style_ads_total(df_ads),
                use_container_width=True,
                hide_index=True,
                height=len(rows_ads) * _ADS_ROW_H + _ADS_HDR_H,
                column_config={
                    "素材名稱":   st.column_config.TextColumn("素材名稱",   width="large"),
                    "曝光":       st.column_config.TextColumn("曝光",       width="small"),
                    "點擊":       st.column_config.TextColumn("點擊",       width="small"),
                    "點閱率":     st.column_config.TextColumn("點閱率",     width="small"),
                    "點擊成本":   st.column_config.TextColumn("點擊成本",   width="small"),
                    "連結點擊":   st.column_config.TextColumn("連結點擊",   width="small"),
                    "連結點擊率": st.column_config.TextColumn("連結點擊率", width="small"),
                    "加購":       st.column_config.TextColumn("加購",       width="small"),
                    "加購率":     st.column_config.TextColumn("加購率",     width="small"),
                    "結帳":       st.column_config.TextColumn("結帳",       width="small"),
                    "購買":       st.column_config.TextColumn("購買",       width="small"),
                    "ROAS":       st.column_config.ProgressColumn(
                                      "ROAS", min_value=0, max_value=roas_max,
                                      format="%.2f", width="medium",
                                  ),
                    "CPA":        st.column_config.TextColumn("CPA",        width="small"),
                    "客單價":     st.column_config.TextColumn("客單價",     width="small"),
                    "轉換率":     st.column_config.TextColumn("轉換率",     width="small"),
                    "花費":       st.column_config.TextColumn("花費",       width="small"),
                },
            )
    else:
        st.info("本期無素材資料")

# ══════════════════════════════════════════════════════════════════════════════
# GA4 頁
# ══════════════════════════════════════════════════════════════════════════════
with tab_ga4:
    with st.spinner("📡 連接 GA4..."):
        ga4_data, ga4_err = load_ga4(since, until, compare_since, compare_until)

    if ga4_err or ga4_data is None:
        st.error(f"⚠️ GA4 資料載入失敗：{ga4_err}")
        st.stop()

    gs  = ga4_data.get("summary", {})
    gcs = ga4_data.get("compare_summary", {})

    st.markdown(f'''
<div class="ga4-hd" style="background:linear-gradient(135deg,#B45309 0%,{GA4_PRIMARY} 60%,{GA4_AMBER} 100%);
            border-radius:14px;padding:18px 24px;margin-bottom:16px;
            display:flex;align-items:center;justify-content:space-between;gap:12px">
  <div style="min-width:0">
    <div style="color:rgba(255,255,255,.7);font-size:10px;font-weight:700;
                text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px;white-space:nowrap">
      Google Analytics 4 · 網站流量分析
    </div>
    <div class="ga4-hd-title" style="color:#fff;font-size:1.4rem;font-weight:900;line-height:1.1;white-space:nowrap">網站流量 × 用戶行為</div>
  </div>
  <div class="ga4-hd-date" style="text-align:right;color:rgba(255,255,255,.85);font-size:13px;flex-shrink:0;white-space:nowrap">{since} ～ {until}</div>
</div>
''', unsafe_allow_html=True)

    st.markdown('<div class="sec-hd">本期網站摘要</div>', unsafe_allow_html=True)
    dur     = gs.get("avg_session_duration", 0)
    dur_fmt = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur > 0 else "—"
    dur_c   = gcs.get("avg_session_duration", 0) or 0
    st.markdown(kpi_html([
        dict(label="工作階段",   value=f"{gs.get('sessions', 0):,}",
             delta=_chg_delta(gs.get("sessions", 0), gcs.get("sessions")),   color=GA4_PRIMARY),
        dict(label="網頁瀏覽數", value=f"{gs.get('pageviews', 0):,}",
             delta=_chg_delta(gs.get("pageviews", 0), gcs.get("pageviews")), color="#E8960A"),
        dict(label="不重複訪客", value=f"{gs.get('total_users', 0):,}",
             delta=_chg_delta(gs.get("total_users", 0), gcs.get("total_users")), color=GA4_AMBER),
        dict(label="新訪客",     value=f"{gs.get('new_users', 0):,}",
             delta=_chg_delta(gs.get("new_users", 0), gcs.get("new_users")), color="#D97706"),
        dict(label="互動率",     value=f"{gs.get('engagement_rate', 0):.1f}%",
             delta=_chg_delta(gs.get("engagement_rate", 0), gcs.get("engagement_rate")), color="#B45309"),
        dict(label="平均停留",   value=dur_fmt,
             delta=_chg_delta(dur, dur_c) if dur_c > 0 else None, color="#92400E"),
        dict(label="跳出率",     value=f"{gs.get('bounce_rate', 0):.1f}%",
             delta=_chg_delta(gs.get("bounce_rate", 0), gcs.get("bounce_rate")),
             color="#DC2626", inverse=True),
    ], cols=7, card_bg="#FFFDF8"), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    def _fmt_dur(sec):
        if not sec: return "0:00"
        m = int(float(sec) // 60); s = int(float(sec) % 60)
        return f"{m}:{s:02d}"

    def _style_pct(val):
        """超過 ±30% 的變化欄位上色（綠=提升，紅=下滑）"""
        if not isinstance(val, str) or val == "—": return ""
        try:
            n = float(val.replace("%", "").replace("+", ""))
            if n >= 30:  return "background-color:rgba(16,185,129,.22);color:#065F46;font-weight:700"
            if n <= -30: return "background-color:rgba(220,38,38,.18);color:#991B1B;font-weight:700"
        except Exception:
            pass
        return ""

    _TOTAL_BG = "background-color:#EDE8DF;font-weight:700;color:#2D1F0F"
    _ROW_H    = 35   # Streamlit dataframe 實際行高 ≈ 35px
    _HDR_H    = 38   # 標題列高度

    def _apply_total_style(df):
        """最後一列（總計）套用淡底色，空白列保持透明"""
        def _row_style(row):
            if row.name == len(df) - 1:
                return [_TOTAL_BG] * len(row)
            return [''] * len(row)
        return df.style.apply(_row_style, axis=1)

    def _style_table(df, vs_cols):
        """總計底色 + vs% 色塊（含總計列）"""
        s = _apply_total_style(df)
        if vs_cols:
            s = s.map(_style_pct, subset=vs_cols)
        return s

    def _prev_t(curr, chg):
        """由當期值 + %chg 還原前期值；chg=-100% 時分母為 0，回傳 0"""
        if chg is None: return 0.0
        denom = 1 + chg / 100
        if abs(denom) < 1e-9: return 0.0
        return curr / denom

    def _chg_t(curr, prev):
        """總計列 vs% 計算"""
        if not prev: return None
        return round((curr - prev) / prev * 100, 1)

    def _pin_total(data_rows, total_row, target_rows=18):
        """填充空白列後把總計固定在最底部"""
        empty_n = max(0, target_rows - len(data_rows) - 1)
        blank   = {k: "" for k in total_row.keys()}
        all_rows = list(data_rows) + [blank] * empty_n + [total_row]
        height   = len(all_rows) * _ROW_H + _HDR_H
        return all_rows, height

    # 流量來源
    st.markdown('<div class="sec-hd">工作階段來源／媒介</div>', unsafe_allow_html=True)
    traffic = ga4_data.get("traffic_sources", [])
    if traffic:
        def _vs(v): return f"{v:+.1f}%" if v is not None else "—"
        rows_t = [{
            "來源／媒介":    r["source"],
            "工作階段":      f"{r['sessions']:,}",
            "工作階段 vs%":  _vs(r["sessions_chg"]),
            "互動工作階段":  f"{r['engaged_sessions']:,}",
            "互動階段 vs%":  _vs(r.get("engaged_sessions_chg")),
            "參與度":        f"{r['engagement_rate']:.1f}%",
            "參與度 vs%":    _vs(r.get("engagement_rate_chg")),
            "平均停留":      r["avg_duration_fmt"],
            "停留 vs%":      _vs(r.get("avg_duration_chg")),
            "事件計數":      f"{r['event_count']:,}",
            "事件 vs%":      _vs(r.get("event_count_chg")),
            "重要事件":      f"{r['key_events']:,}",
            "重要事件 vs%":  _vs(r.get("key_events_chg")),
            "重要事件率":    f"{r['key_event_rate']:.2f}%",
            "事件率 vs%":    _vs(r.get("key_event_rate_chg")),
            "總收益":        f"${r['revenue']:,.0f}" if r["revenue"] > 0 else "—",
            "收益 vs%":      _vs(r.get("revenue_chg")),
        } for r in traffic]
        # 當期總計
        tot_sess  = sum(r["sessions"] for r in traffic)
        tot_eng   = sum(r["engaged_sessions"] for r in traffic)
        tot_ev    = sum(r["event_count"] for r in traffic)
        tot_ke    = sum(r["key_events"] for r in traffic)
        tot_rev   = sum(r["revenue"] for r in traffic)
        tot_dur   = (sum(r["avg_duration"] * r["sessions"] for r in traffic) / tot_sess) if tot_sess > 0 else 0
        tot_eng_r = round(tot_eng / tot_sess * 100, 1) if tot_sess > 0 else 0
        tot_ker   = round(tot_ke  / tot_sess * 100, 2) if tot_sess > 0 else 0
        # 前期總計（由 chg% 反推）
        prev_sess = sum(_prev_t(r["sessions"],        r["sessions_chg"])               for r in traffic)
        prev_eng  = sum(_prev_t(r["engaged_sessions"],r.get("engaged_sessions_chg"))   for r in traffic)
        prev_ev   = sum(_prev_t(r["event_count"],     r.get("event_count_chg"))        for r in traffic)
        prev_ke   = sum(_prev_t(r["key_events"],      r.get("key_events_chg"))         for r in traffic)
        prev_rev  = sum(_prev_t(r["revenue"],         r.get("revenue_chg"))            for r in traffic)
        prev_dur_n= sum(_prev_t(r["avg_duration"],    r.get("avg_duration_chg")) *
                        _prev_t(r["sessions"],        r["sessions_chg"])               for r in traffic)
        prev_dur  = prev_dur_n / prev_sess if prev_sess > 0 else 0
        prev_eng_r= round(prev_eng / prev_sess * 100, 1) if prev_sess > 0 else 0
        prev_ker  = round(prev_ke  / prev_sess * 100, 2) if prev_sess > 0 else 0
        total_row_t = {
            "來源／媒介":    "總計",
            "工作階段":      f"{tot_sess:,}",
            "工作階段 vs%":  _vs(_chg_t(tot_sess,  prev_sess)),
            "互動工作階段":  f"{tot_eng:,}",
            "互動階段 vs%":  _vs(_chg_t(tot_eng,   prev_eng)),
            "參與度":        f"{tot_eng_r:.1f}%",
            "參與度 vs%":    _vs(_chg_t(tot_eng_r, prev_eng_r)),
            "平均停留":      _fmt_dur(tot_dur),
            "停留 vs%":      _vs(_chg_t(tot_dur,   prev_dur)),
            "事件計數":      f"{tot_ev:,}",
            "事件 vs%":      _vs(_chg_t(tot_ev,    prev_ev)),
            "重要事件":      f"{tot_ke:,}",
            "重要事件 vs%":  _vs(_chg_t(tot_ke,    prev_ke)),
            "重要事件率":    f"{tot_ker:.2f}%",
            "事件率 vs%":    _vs(_chg_t(tot_ker,   prev_ker)),
            "總收益":        f"${tot_rev:,.0f}" if tot_rev > 0 else "—",
            "收益 vs%":      _vs(_chg_t(tot_rev,   prev_rev)),
        }
        all_rows_t, h_t = _pin_total(rows_t, total_row_t, target_rows=18)
        df_t = pd.DataFrame(all_rows_t)
        _vs_t = [c for c in df_t.columns if "vs%" in c]
        st.dataframe(
            _style_table(df_t, _vs_t),
            use_container_width=True, hide_index=True,
            height=h_t,
        )
    else:
        st.info("流量來源資料不足")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # 網頁路徑
    st.markdown('<div class="sec-hd">網頁路徑參與表現</div>', unsafe_allow_html=True)
    pages_data = ga4_data.get("pages", [])
    if pages_data:
        rows_p = [{
            "網頁路徑":     r["path"][:50],
            "瀏覽":         f"{r['views']:,}",
            "瀏覽 vs%":     _vs(r.get("views_chg")),
            "活躍使用者":   f"{r['active_users']:,}",
            "使用者 vs%":   _vs(r.get("active_users_chg")),
            "每人觀看數":   f"{r['views_per_user']:.2f}",
            "平均參與時間": r["avg_dur_per_user_fmt"],
            "停留 vs%":     _vs(r.get("avg_dur_per_user_chg")),
            "事件計數":     f"{r['event_count']:,}",
            "事件 vs%":     _vs(r.get("event_count_chg")),
            "重要事件":     f"{r['key_events']:,}",
            "重要事件 vs%": _vs(r.get("key_events_chg")),
            "總收益":       f"${r['revenue']:,.0f}" if r["revenue"] > 0 else "—",
            "收益 vs%":     _vs(r.get("revenue_chg")),
        } for r in pages_data]
        # 當期總計
        tot_v    = sum(r["views"] for r in pages_data)
        tot_u    = sum(r["active_users"] for r in pages_data)
        tot_pe   = sum(r["event_count"] for r in pages_data)
        tot_pke  = sum(r["key_events"] for r in pages_data)
        tot_pr   = sum(r["revenue"] for r in pages_data)
        tot_vpu  = round(tot_v / tot_u, 2) if tot_u > 0 else 0
        tot_dur_p = (sum(r["avg_dur_per_user"] * r["active_users"] for r in pages_data) / tot_u) if tot_u > 0 else 0
        # 前期總計（由 chg% 反推）
        prev_v   = sum(_prev_t(r["views"],          r.get("views_chg"))          for r in pages_data)
        prev_u   = sum(_prev_t(r["active_users"],   r.get("active_users_chg"))   for r in pages_data)
        prev_pe  = sum(_prev_t(r["event_count"],    r.get("event_count_chg"))    for r in pages_data)
        prev_pke = sum(_prev_t(r["key_events"],     r.get("key_events_chg"))     for r in pages_data)
        prev_pr  = sum(_prev_t(r["revenue"],        r.get("revenue_chg"))        for r in pages_data)
        prev_du_n= sum(_prev_t(r["avg_dur_per_user"],r.get("avg_dur_per_user_chg")) *
                       _prev_t(r["active_users"],   r.get("active_users_chg"))   for r in pages_data)
        prev_dur_p = prev_du_n / prev_u if prev_u > 0 else 0
        prev_vpu   = round(prev_v / prev_u, 2) if prev_u > 0 else 0
        total_row_p = {
            "網頁路徑":     "總計",
            "瀏覽":         f"{tot_v:,}",     "瀏覽 vs%":     _vs(_chg_t(tot_v,    prev_v)),
            "活躍使用者":   f"{tot_u:,}",     "使用者 vs%":   _vs(_chg_t(tot_u,    prev_u)),
            "每人觀看數":   f"{tot_vpu:.2f}",
            "平均參與時間": _fmt_dur(tot_dur_p),"停留 vs%":    _vs(_chg_t(tot_dur_p,prev_dur_p)),
            "事件計數":     f"{tot_pe:,}",    "事件 vs%":     _vs(_chg_t(tot_pe,   prev_pe)),
            "重要事件":     f"{tot_pke:,}",   "重要事件 vs%": _vs(_chg_t(tot_pke,  prev_pke)),
            "總收益":       f"${tot_pr:,.0f}" if tot_pr > 0 else "—",
            "收益 vs%":     _vs(_chg_t(tot_pr, prev_pr)),
        }
        all_rows_p, h_p = _pin_total(rows_p, total_row_p, target_rows=22)
        df_p = pd.DataFrame(all_rows_p)
        _vs_p = [c for c in df_p.columns if "vs%" in c]
        st.dataframe(
            _style_table(df_p, _vs_p),
            use_container_width=True, hide_index=True,
            height=h_p,
        )
    else:
        st.info("網頁路徑資料不足")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # 商品表現
    st.markdown('<div class="sec-hd">商品表現（購買紀錄）</div>', unsafe_allow_html=True)
    products = ga4_data.get("products", [])
    if products:
        rows_prod = [{
            "商品名稱":   r["name"][:35],
            "購買數":     f"{r['purchases']:,}",
            "購買 vs%":   _vs(r.get("purchases_chg")),
            "商品收益":   f"${r['revenue']:,.0f}" if r["revenue"] > 0 else "—",
            "收益 vs%":   _vs(r.get("revenue_chg")),
            "平均客單價": f"${r['aov']:,.0f}" if r.get("aov", 0) > 0 else "—",
            "客單價 vs%": _vs(r.get("aov_chg")),
        } for r in products]
        # 當期總計
        tot_pur   = sum(r["purchases"] for r in products)
        tot_rev_p = sum(r["revenue"]   for r in products)
        tot_aov   = round(tot_rev_p / tot_pur, 0) if tot_pur > 0 else 0
        # 前期總計（由 chg% 反推）
        prev_pur  = sum(_prev_t(r["purchases"], r.get("purchases_chg")) for r in products)
        prev_rev_p= sum(_prev_t(r["revenue"],   r.get("revenue_chg"))   for r in products)
        prev_aov  = round(prev_rev_p / prev_pur, 0) if prev_pur > 0 else 0
        total_row_prod = {
            "商品名稱":   "總計",
            "購買數":     f"{tot_pur:,}",
            "購買 vs%":   _vs(_chg_t(tot_pur,   prev_pur)),
            "商品收益":   f"${tot_rev_p:,.0f}" if tot_rev_p > 0 else "—",
            "收益 vs%":   _vs(_chg_t(tot_rev_p, prev_rev_p)),
            "平均客單價": f"${tot_aov:,.0f}" if tot_aov > 0 else "—",
            "客單價 vs%": _vs(_chg_t(tot_aov,   prev_aov)),
        }
        all_rows_prod, h_prod = _pin_total(rows_prod, total_row_prod, target_rows=14)
        df_prod = pd.DataFrame(all_rows_prod)
        _vs_prod = [c for c in df_prod.columns if "vs%" in c]
        st.dataframe(
            _style_table(df_prod, _vs_prod),
            use_container_width=True, hide_index=True,
            height=h_prod,
        )
    else:
        st.info("本期無商品購買記錄")

# FOOTER
st.markdown(f"""
<div class="dash-footer">
  <b style="color:#2D1F0F">采姸 CHAI YAN · Since 1991</b>　|
  Meta Marketing API v21.0 × Google Analytics 4　|　每 30 分鐘自動刷新　|
  {datetime.now().strftime('%Y/%m/%d %H:%M')} 產出
</div>
""", unsafe_allow_html=True)
