import streamlit as st
import yfinance as yf
import pandas as pd
import random

st.set_page_config(page_title="China Stock Recommender", layout="wide")

st.title("📈 China Stock Recommendation & Live Market Data")

# ===== Sidebar =====
with st.sidebar:
    st.header("Search a Stock")
    default_code = "600519.SS"  # Default: Kweichow Moutai
    code = st.text_input("Enter stock symbol (e.g. 600519.SS or 000001.SZ)", value=default_code)
    period = st.selectbox("Select time period", ["5d", "1mo", "3mo", "6mo", "1y"], index=1)
    if st.button("Search"):
        st.session_state['search'] = True

if 'search' not in st.session_state:
    st.session_state['search'] = False

# ===== Helper function =====
def get_stock_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except Exception as e:
        st.error(f"Failed to retrieve stock data: {e}")
        return None, None

# ===== Main Display =====
if st.session_state['search'] or code:
    st.subheader(f"🎯 Current Stock: {code}")
    hist, info = get_stock_data(code, period=period)

    if hist is not None and not hist.empty:
        current_price = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else current_price
        diff = current_price - prev_close
        pct = diff / prev_close * 100

        col1, col2 = st.columns(2)
        col1.metric("Current Price (¥)", f"{current_price:.2f}", f"{diff:+.2f} ({pct:+.2f}%)")

        if info.get("longName"):
            col2.write(f"**Company:** {info['longName']}")
        if info.get("sector"):
            col2.write(f"**Sector:** {info['sector']}")

        st.line_chart(hist["Close"], use_container_width=True)

        # ===== Recommendations (sample list) =====
        st.subheader("📊 Similar Stock Recommendations")
        sample_stocks = ["600000.SS", "600036.SS", "000002.SZ", "000651.SZ", "601318.SS", "300750.SZ"]
        recs = random.sample(sample_stocks, 3)
        for s in recs:
            st.write(f"- 💡 Recommended: `{s}`  [View on EastMoney](https://quote.eastmoney.com/{s}.html)")
    else:
        st.warning("No stock data found. Please check the symbol and try again.")

st.markdown("---")
st.caption("Data source: Yahoo Finance (free public data, for demo only)")
