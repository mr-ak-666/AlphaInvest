# -*- coding: utf-8 -*-
import time
import requests
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# --- Optional TA imports (graceful degrade if not installed) ---
TA_AVAILABLE = True
try:
    from ta.trend import SMAIndicator, MACD
    from ta.momentum import RSIIndicator
    from ta.volatility import BollingerBands
except Exception:
    TA_AVAILABLE = False

# ==================== Page Setup ====================
st.set_page_config(page_title="Stock Dashboard (Reliable)", page_icon="📈", layout="wide")
st.title("📈 Stock Analysis Dashboard")

# ==================== Sidebar =======================
st.sidebar.header("⚙️ Settings")

# --- Data & refresh controls ---
symbol_input = st.sidebar.text_input(
    "Stock Symbol",
    "RELIANCE.NS",
    help="Examples: AAPL (US), TCS.NS (NSE), RELIANCE.NS, INFY.NS, TCS.BO"
)
period_choice = st.sidebar.selectbox(
    "Time Period",
    ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y", "MAX"],
    index=6  # default to 5Y for India use-case
)

INTERVAL_MAP = {
    "1D": ["1m", "2m", "5m", "15m", "30m", "60m"],
    "5D": ["1m", "2m", "5m", "15m", "30m", "60m", "90m"],
    "1M": ["30m", "60m", "90m", "1d"],
    "3M": ["1d", "5d", "1wk"],
    "6M": ["1d", "5d", "1wk"],
    "1Y": ["1d", "5d", "1wk", "1mo"],
    "5Y": ["1wk", "1mo"],
    "MAX": ["1mo", "3mo"]
}
interval_choice = st.sidebar.selectbox("Interval", INTERVAL_MAP.get(period_choice, ["1d"]))

# --- Real-time auto-refresh for intraday ---
st.sidebar.subheader("⏱️ Live Update")
auto_refresh = st.sidebar.checkbox("Auto-refresh during market hours", value=True)
refresh_sec = st.sidebar.slider("Refresh every (seconds)", 15, 90, 60, help="For 1m view, 60s is typical.")

# --- Optional external free APIs (toggle if you want extra fundamentals/news) ---
st.sidebar.subheader("🛰️ External Free APIs (Optional)")
use_indian_open_api = st.sidebar.checkbox("Indian Stock Market API (real-time price)", value=False,
                                          help="Open-source price API via Yahoo. Fallback if Yahoo is flaky.")
use_indian_info_api = st.sidebar.checkbox("Indian Stock Exchange API (rich details)", value=False,
                                          help="Attempts to fetch extra fundamentals, corporate actions, news.")

st.sidebar.subheader("📐 Indicators")
show_sma = st.sidebar.checkbox("SMA (20/50)", True)
show_bb = st.sidebar.checkbox("Bollinger Bands", True)
show_rsi = st.sidebar.checkbox("RSI", True)
show_macd = st.sidebar.checkbox("MACD", True)
show_volume = st.sidebar.checkbox("Volume", True)

if not TA_AVAILABLE and (show_sma or show_bb or show_rsi or show_macd):
    st.sidebar.warning("`ta` library not found — indicators will be skipped.\nInstall: pip install ta")

# ==================== Utilities =====================
PERIOD_MAP = {"1D": "1d", "5D": "5d", "1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "5Y": "5y", "MAX": "max"}
COMMON_US = {"AAPL","MSFT","GOOGL","GOOG","TSLA","NVDA","AMZN","META","NFLX","AMD","INTC","AVGO"}

# Known aliases/renames that sometimes help when Yahoo is flaky
ALIASES = {
    "KPIT.NS": ["KPITTECH.NS", "KPIT.BO", "KPITTECH.BO"],
}

INDIAN_OPEN_API_BASE = "https://military-jobye-haiqstudios-14f59639.koyeb.app"
INDIAN_INFO_API_BASE = "https://indianapi.in"

def normalize_symbol(sym: str) -> str:
    """Auto-append NSE (.NS) for bare Indian symbols; keep known US intact."""
    s = (sym or "").strip().upper()
    if not s:
        return s
    if any(s.endswith(suf) for suf in (".NS",".BO",".NSE",".BSE",".TO",".L",".HK",".AX",".SA",".PA",".F",".SW",".NE")):
        return s
    # If short alphabetic and not a common US mega-cap, assume NSE
    if s.isalpha() and 1 <= len(s) <= 6 and s not in COMMON_US:
        return s + ".NS"
    return s

def clamp_period_interval(period_key: str, interval_ui: str):
    """
    Valid combinations:
    - 1m/2m => period <= 7d (we force to 5d)
    - 5m..90m => period <= 60d (force to 6mo for longer periods)
    - 1d/1wk/1mo => any period
    """
    period = PERIOD_MAP[period_key]
    interval = interval_ui
    if interval in {"1m","2m"} and period not in {"1d","5d"}:
        period = "5d"
    elif interval in {"5m","15m","30m","60m","90m"} and period in {"1y","5y","max"}:
        period = "6mo"
    return period, interval

def _download(sym: str, period: str, interval: str) -> pd.DataFrame:
    kwargs = dict(period=period, interval=interval, auto_adjust=False, progress=False, threads=False, rounding=True)
    try:
        return yf.download(sym, repair=True, **kwargs)
    except TypeError:
        # Older yfinance may not support repair; retry without
        return yf.download(sym, **kwargs)

def _history(sym: str, period: str, interval: str) -> pd.DataFrame:
    t = yf.Ticker(sym)
    return t.history(period=period, interval=interval, auto_adjust=False, actions=False)

def _date_range(sym: str, interval: str, days: int) -> pd.DataFrame:
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    kwargs = dict(start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"),
                  interval=interval, auto_adjust=False, progress=False, threads=False, rounding=True)
    try:
        return yf.download(sym, repair=True, **kwargs)
    except TypeError:
        return yf.download(sym, **kwargs)

def _try_info(sym: str) -> dict:
    info = {}
    try:
        t = yf.Ticker(sym)
        fi = getattr(t, "fast_info", {}) or {}
        info.update({
            "market_cap": fi.get("market_cap"),
            "previous_close": fi.get("previous_close"),
            "last_price": fi.get("last_price"),
            "currency": fi.get("currency")
        })
        full = getattr(t, "info", {}) or {}
        info.update({
            "longName": full.get("longName"),
            "sector": full.get("sector"),
            "industry": full.get("industry"),
            "country": full.get("country"),
            "website": full.get("website"),
            "employees": full.get("fullTimeEmployees"),
            "trailingPE": full.get("trailingPE"),
            "trailingEps": full.get("trailingEps"),
            "fiftyTwoWeekHigh": full.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": full.get("fiftyTwoWeekLow"),
            "dividendYield": full.get("dividendYield"),
            "beta": full.get("beta"),
            "longBusinessSummary": full.get("longBusinessSummary"),
        })
    except Exception:
        pass
    return info

def _currency_symbol(sym_used: str, info: dict) -> str:
    # Prefer Yahoo currency if available
    cur = (info or {}).get("currency")
    if cur == "INR" or (sym_used.endswith(".NS") or sym_used.endswith(".BO")):
        return "₹"
    return "$"

# ---------- Optional external free APIs ----------
def fetch_indian_open_api_price(symbol: str):
    """Fetch real-time price via open-source Indian Stock Market API (optional)."""
    try:
        url = f"{INDIAN_OPEN_API_BASE}/stock?symbol={symbol}"
        r = requests.get(url, timeout=6)
        if r.ok:
            js = r.json()
            # Tries to get a float price field; adapt if schema differs
            for key in ("current_price", "price", "ltp", "last_price"):
                if isinstance(js, dict) and key in js:
                    return float(js[key])
                if isinstance(js, dict) and "data" in js and key in js["data"]:
                    return float(js["data"][key])
    except Exception:
        pass
    return None

def fetch_indian_info_api(name_or_symbol: str) -> dict:
    """
    Fetch richer details (fundamentals, corporate actions, news) from Indian Stock Exchange API.
    Safe optional call; returns {} on failure.
    """
    try:
        # This API usually expects company name; pass symbol without suffix for better hits
        q = name_or_symbol.replace(".NS","").replace(".BO","")
        url = f"{INDIAN_INFO_API_BASE}/stock?name={q}"
        r = requests.get(url, timeout=8)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return {}

@st.cache_data(ttl=120, show_spinner=False)
def fetch_resilient(symbol_raw: str, period_key: str, interval_ui: str, retries: int = 3):
    """
    Attempts:
    1) normalized symbol with yf.download(period/interval)
    2) .history(period/interval)
    3) date-range fallback (365d for daily, 30d for intraday)
    4) try aliases (e.g., KPITTECH.NS) in same order
    """
    norm = normalize_symbol(symbol_raw)
    period, interval = clamp_period_interval(period_key, interval_ui)
    candidates = [norm] + ALIASES.get(norm, [])
    last_exc = None

    for sym in candidates:
        # 1) yf.download with retries
        for attempt in range(retries):
            try:
                df = _download(sym, period, interval)
                if df is not None and not df.empty and "Close" in df.columns:
                    info = _try_info(sym)
                    return df.dropna(subset=["Close"]), info, sym, period, interval, f"download({period},{interval})"
            except Exception as e:
                last_exc = e
            time.sleep(0.8 * (attempt + 1))

        # 2) Ticker.history
        try:
            df2 = _history(sym, period, interval)
            if df2 is not None and not df2.empty and "Close" in df2.columns:
                info = _try_info(sym)
                return df2.dropna(subset=["Close"]), info, sym, period, interval, f"history({period},{interval})"
        except Exception as e:
            last_exc = e

        # 3) Date-range fallback
        try:
            if interval in {"1d","1wk","1mo"}:
                df3 = _date_range(sym, interval, days=365)
            else:
                df3 = _date_range(sym, interval, days=30)
            if df3 is not None and not df3.empty and "Close" in df3.columns:
                info = _try_info(sym)
                return df3.dropna(subset=["Close"]), info, sym, period, interval, f"daterange({interval})"
        except Exception as e:
            last_exc = e

    raise RuntimeError(
        f"No data for {norm} (period={period}, interval={interval}). "
        f"Tried aliases: {candidates}. Last error: {last_exc}"
    )

@st.cache_data(ttl=900, show_spinner=False)
def fetch_history_5y_plus(sym_raw: str, prefer_max: bool = False) -> pd.DataFrame:
    """
    Dedicated function to fetch long history for training/backtests.
    Uses daily bars (or weekly/monthly via resample if needed).
    """
    sym = normalize_symbol(sym_raw)
    t = yf.Ticker(sym)
    period = "max" if prefer_max else "5y"
    try:
        df = t.history(period=period, interval="1d", auto_adjust=False, actions=False)
    except Exception:
        df = yf.download(sym, period=("max" if prefer_max else "5y"), interval="1d", progress=False, threads=False)
    if df is None or df.empty:
        return pd.DataFrame()
    # Clean
    df = df.dropna(subset=["Close"])
    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute indicators only if TA_AVAILABLE."""
    if df.empty or not TA_AVAILABLE:
        return df
    out = df.copy()
    try:
        out["SMA20"] = SMAIndicator(out["Close"], 20).sma_indicator()
        out["SMA50"] = SMAIndicator(out["Close"], 50).sma_indicator()
    except Exception:
        pass
    try:
        bb = BollingerBands(out["Close"])
        out["BB_H"] = bb.bollinger_hband()
        out["BB_L"] = bb.bollinger_lband()
        out["BB_M"] = bb.bollinger_mavg()
    except Exception:
        pass
    try:
        out["RSI"] = RSIIndicator(out["Close"]).rsi()
    except Exception:
        pass
    try:
        macd = MACD(out["Close"])
        out["MACD"] = macd.macd()
        out["MACD_SIGNAL"] = macd.macd_signal()
        out["MACD_HIST"] = macd.macd_diff()
    except Exception:
        pass
    return out

def colored_volume(df: pd.DataFrame):
    if df.empty or "Open" not in df.columns or "Close" not in df.columns:
        return []
    return ["#ef5350" if c < o else "#26a69a" for o, c in zip(df["Open"], df["Close"])]

# ==================== Auto-refresh (intraday) ====================
if auto_refresh and interval_choice in {"1m","2m","5m","15m","30m","60m","90m"}:
    # Use Streamlit's built-in autorefresh to re-run app
    st.experimental_set_query_params(_=str(int(time.time())))  # bust query cache keys
    st.autorefresh = st.experimental_rerun  # alias for clarity (forward compat)

# ==================== Fetch & Prepare ====================
with st.spinner(f"Fetching {symbol_input} · {period_choice}/{interval_choice} ..."):
    try:
        df, info, symbol_used, period_used, interval_used, fetch_mode = fetch_resilient(
            symbol_input, period_choice, interval_choice
        )
    except Exception as e:
        st.error(f"❌ {e}")
        st.info(
            "Quick tips:\n"
            "- India: **.NS** (NSE) / **.BO** (BSE), e.g., **TCS.NS**, **KPIT.NS**\n"
            "- For 1m/2m intervals, use period ≤ **5d** (Yahoo limitation)\n"
            "- Try **AAPL** with **1Y/1d** to verify network\n"
            "- Update yfinance: `pip install --upgrade yfinance`"
        )
        st.stop()

st.caption(f"Symbol: {symbol_used} • Period: {period_used} • Interval: {interval_used} • Mode: {fetch_mode} • Rows: {len(df)}")

# Indicators (optional)
df = add_indicators(df)

# --- Long history dataset (5Y+ for AI training/backtests) ---
hist_df = fetch_history_5y_plus(symbol_input, prefer_max=(period_choice == "MAX"))

# ==================== Metrics ====================
try:
    current_price = float(df["Close"].iloc[-1])
    prev_close = float(info.get("previous_close") or (df["Close"].iloc[-2] if len(df) > 1 else df["Close"].iloc[-1]))
    chg = current_price - prev_close
    chg_pct = (chg / prev_close * 100) if prev_close else 0.0
    day_high = float(df["High"].iloc[-1])
    day_low = float(df["Low"].iloc[-1])
    last_vol = int(df["Volume"].iloc[-1]) if "Volume" in df.columns else 0
except Exception:
    current_price = df["Close"].iloc[-1]
    prev_close, chg, chg_pct, day_high, day_low, last_vol = None, None, None, None, None, None

# Optional: override current_price with external real-time API if enabled
if use_indian_open_api:
    alt_price = fetch_indian_open_api_price(symbol_used)
    if isinstance(alt_price, (int, float)) and pd.notna(alt_price):
        current_price = float(alt_price)

cur_symbol = _currency_symbol(symbol_used, info)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(f"{symbol_used} Price", f"{cur_symbol}{current_price:,.2f}" if pd.notna(current_price) else "N/A",
          f"{(chg if chg is not None else 0):+.2f} ({(chg_pct if chg_pct is not None else 0):+.2f}%)")
c2.metric("High (Last Bar)", f"{cur_symbol}{day_high:,.2f}" if day_high is not None else "N/A")
c3.metric("Low (Last Bar)", f"{cur_symbol}{day_low:,.2f}" if day_low is not None else "N/A")
c4.metric("Volume (Last Bar)", f"{last_vol:,}" if last_vol is not None else "N/A")
mcap = info.get("market_cap")
c5.metric("Market Cap", f"{cur_symbol}{mcap/1e9:,.2f}B" if mcap else "N/A")

st.markdown("---")

# ==================== Main Chart ====================
st.subheader("📊 Price Chart")

rows = 1 + int(TA_AVAILABLE and show_rsi) + int(TA_AVAILABLE and show_macd)
row_heights = [0.6] + [0.2] * (rows - 1)
titles = ["Price"] + (["RSI"] if TA_AVAILABLE and show_rsi else []) + (["MACD"] if TA_AVAILABLE and show_macd else [])

fig = make_subplots(
    rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.04,
    row_heights=row_heights, subplot_titles=titles
)

# Candles
fig.add_trace(
    go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name="Price", increasing_line_color="#26a69a", decreasing_line_color="#ef5350"
    ),
    row=1, col=1
)

# SMA
if TA_AVAILABLE and show_sma and "SMA20" in df and "SMA50" in df:
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA20"], name="SMA 20", line=dict(color="orange", width=1.4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA50"], name="SMA 50", line=dict(color="steelblue", width=1.4)), row=1, col=1)

# Bollinger
if TA_AVAILABLE and show_bb and "BB_H" in df:
    fig.add_trace(go.Scatter(x=df.index, y=df["BB_H"], name="BB High", line=dict(color="gray", width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["BB_L"], name="BB Low", line=dict(color="gray", width=1)), row=1, col=1)
    if "BB_M" in df:
        fig.add_trace(go.Scatter(x=df.index, y=df["BB_M"], name="BB Mid", line=dict(color="goldenrod", width=1)), row=1, col=1)

# RSI
current_row = 1
if TA_AVAILABLE and show_rsi and "RSI" in df:
    current_row += 1
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI", line=dict(color="purple", width=2)), row=current_row, col=1)
    # Horizontal guides
    fig.add_trace(go.Scatter(x=df.index, y=[70]*len(df), name="RSI 70", line=dict(color="red", width=1, dash="dash"), showlegend=False), row=current_row, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=[30]*len(df), name="RSI 30", line=dict(color="green", width=1, dash="dash"), showlegend=False), row=current_row, col=1)
    fig.update_yaxes(title_text="RSI", row=current_row, col=1)

# MACD
if TA_AVAILABLE and show_macd and "MACD" in df:
    current_row += 1
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD", line=dict(color="blue", width=2)), row=current_row, col=1)
    if "MACD_SIGNAL" in df:
        fig.add_trace(go.Scatter(x=df.index, y=df["MACD_SIGNAL"], name="Signal", line=dict(color="orange", width=2)), row=current_row, col=1)
    if "MACD_HIST" in df:
        fig.add_trace(go.Bar(x=df.index, y=df["MACD_HIST"], name="Hist", marker_color="gray", opacity=0.4), row=current_row, col=1)
    fig.update_yaxes(title_text="MACD", row=current_row, col=1)

fig.update_layout(height=720, template="plotly_white", hovermode="x unified",
                  xaxis_rangeslider_visible=False, showlegend=True)
fig.update_yaxes(title_text=f"Price ({cur_symbol})", row=1, col=1)
st.plotly_chart(fig, use_container_width=True)

# ==================== Volume ====================
if show_volume and "Volume" in df:
    st.subheader("📦 Volume")
    vol_colors = colored_volume(df)
    vfig = go.Figure()
    vfig.add_trace(go.Bar(x=df.index, y=df["Volume"], marker_color=vol_colors, name="Volume"))
    vfig.update_layout(height=260, template="plotly_white", showlegend=False)
    st.plotly_chart(vfig, use_container_width=True)

# ==================== Company & Financials ====================
st.markdown("---")
colA, colB = st.columns(2)

with colA:
    st.subheader("📋 Company")
    st.write(f"**Name:** {info.get('longName', 'N/A')}")
    st.write(f"**Sector / Industry:** {info.get('sector', 'N/A')} / {info.get('industry', 'N/A')}")
    st.write(f"**Country:** {info.get('country', 'N/A')}")
    site = info.get("website")
    if site:
        st.write(f"**Website:** {site}")
    st.write(f"**Employees:** {info.get('employees', 'N/A')}")
    if info.get("longBusinessSummary"):
        with st.expander("📑 Business Summary"):
            st.write(info["longBusinessSummary"])

with colB:
    st.subheader("💰 Financials (Basic)")
    st.write(f"**P/E (TTM):** {info.get('trailingPE', 'N/A')}")
    st.write(f"**EPS (TTM):** {info.get('trailingEps', 'N/A')}")
    fhi, flo = info.get("fiftyTwoWeekHigh"), info.get("fiftyTwoWeekLow")
    st.write(f"**52W High / Low:** {f'{cur_symbol}{fhi:,.2f}' if fhi else 'N/A'} / {f'{cur_symbol}{flo:,.2f}' if flo else 'N/A'}")
    dy = info.get("dividendYield")
    st.write(f"**Dividend Yield:** {f'{dy*100:.2f}%' if dy else 'N/A'}")
    st.write(f"**Beta:** {info.get('beta', 'N/A')}")

# ---- Optional enriched details from Indian info API ----
if use_indian_info_api:
    extra = fetch_indian_info_api(symbol_used)
    if extra:
        with st.expander("🧠 Extra Details (Indian Info API)"):
            # Show only if keys exist; structure may vary
            # Try to print concise highlights
            highlights = []
            for k in ("companyName","industry","percentChange","yearHigh","yearLow"):
                if k in extra:
                    highlights.append(f"- **{k}**: {extra[k]}")
            if highlights:
                st.markdown("\n".join(highlights))
            # Corporate actions, news (if present)
            if isinstance(extra, dict):
                if "stockCorporateActionData" in extra and extra["stockCorporateActionData"]:
                    st.markdown("**Corporate Actions (snapshot)**")
                    st.json(extra["stockCorporateActionData"])
                if "recentNews" in extra and extra["recentNews"]:
                    st.markdown("**Recent News (snapshot)**")
                    st.json(extra["recentNews"])

# ==================== Recent Data & Download ====================
st.markdown("---")
st.subheader("📅 Recent Trading Data")
cols_to_show = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
recent = df[cols_to_show].tail(10).sort_index(ascending=False)
st.dataframe(recent, use_container_width=True)

csv_bytes = df.to_csv().encode("utf-8")
st.download_button(
    "📥 Download Current View CSV",
    data=csv_bytes,
    file_name=f"{symbol_used}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
)

# ---- Long-history download (5Y+ / MAX) ----
if not hist_df.empty:
    st.subheader("🗄️ Historical (5Y+ / MAX) — Daily")
    hfig = go.Figure()
    hfig.add_trace(go.Scatter(x=hist_df.index, y=hist_df["Close"], name="Close", line=dict(color="#2962ff")))
    hfig.update_layout(height=260, template="plotly_white", showlegend=False)
    st.plotly_chart(hfig, use_container_width=True)

    hist_csv = hist_df.to_csv().encode("utf-8")
    st.download_button(
        "📥 Download Historical Daily CSV (5Y+/MAX)",
        data=hist_csv,
        file_name=f"{symbol_used}_history_daily_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")