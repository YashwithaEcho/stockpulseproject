import streamlit as st
import requests
import pandas as pd
from data_fetcher import fetch_stock_history

# Set up page styling configuration
st.set_page_config(page_title="StockPulse Terminal", layout="wide")

# Backend API server URL definition
BACKEND_URL = "http://127.0.0.1:8000"

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("🎛️ Navigation Panel")
page = st.sidebar.radio("Go To Page:", ["📊 Dashboard", "🔍 Search & Trade", "📜 Transaction History"])

# --- HELPER FUNCTION: FETCH USER PROFILE DATA FROM FASTAPI (Days 1-3 Goal) ---
def get_user_data(username="trader1"):
    try:
        response = requests.get(f"{BACKEND_URL}/user/{username}")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

user_info = get_user_data("trader1")

# Default placeholders if backend isn't up yet
cash_balance = user_info["cash_balance"] if user_info else 10000.00
portfolio_value = user_info["portfolio_holdings_value"] if user_info else 0.00
total_net_worth = user_info["total_net_worth"] if user_info else 10000.00
ledger_data = user_info["current_holdings"] if user_info else []

# --- PAGE 1: DASHBOARD ---
if page == "📊 Dashboard":
    st.title("📈 StockPulse Live Analytics Dashboard")
    st.markdown("Welcome back, **trader1**! Here is your current real-time financial portfolio standing:")
    
    # Render metric boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💰 Virtual Cash Balance", value=f"${cash_balance:,.2f}")
    with col2:
        st.metric(label="📊 Portfolio Asset Value", value=f"${portfolio_value:,.2f}")
    with col3:
        st.metric(label="🏆 Total Combined Net Worth", value=f"${total_net_worth:,.2f}")
        
    st.markdown("---")
    st.subheader("📁 Current Portfolio Holdings")
    if ledger_data:
        df_holdings = pd.DataFrame(ledger_data)
        st.dataframe(df_holdings, use_container_width=True)
    else:
        st.info("You don't own any stock positions yet! Go to the 'Search & Trade' page to execute an order.")

# --- PAGE 2: SEARCH & TRADE ---
elif page == "🔍 Search & Trade":
    st.title("💱 Live Asset Trading Desk")
    
    ticker_input = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA, NVDA):", "AAPL")
    clean_ticker = ticker_input.upper().strip()
    
    # Fetch historical data for generating visual chart (Days 4-5 Goal)
    df_history = fetch_stock_history(clean_ticker, timeframe="1mo")
    
    if df_history is not None and not df_history.empty:
        latest_price = round(float(df_history['Close'].iloc[-1]), 2)
        st.success(f"📟 **Current Market Value for {clean_ticker}:** ${latest_price:.2f}")
        
        # Days 4-5 Goal: Render interactive line chart
        st.subheader(f"📈 30-Day Historical Price Graph for {clean_ticker}")
        st.line_chart(df_history['Close'])
        
        st.markdown("---")
        st.subheader("🛒 Execute Order Transactions")
        
        col1, col2 = st.columns(2)
        with col1:
            shares_buy = st.number_input("Shares to Buy", min_value=1, value=1, step=1)
            # Days 6-7 Goal: Connect Buy Button to backend POST /buy API route
            if st.button("🚀 Execute Buy Order", use_container_width=True):
                res = requests.post(f"{BACKEND_URL}/buy?username=trader1&ticker={clean_ticker}&shares={shares_buy}")
                if res.status_code == 200:
                    st.success(f"Successfully bought {shares_buy} shares of {clean_ticker}!")
                    st.rerun()
                else:
                    st.error(f"Error: {res.json()['detail']}")
                    
        with col2:
            shares_sell = st.number_input("Shares to Sell", min_value=1, value=1, step=1)
            # Days 6-7 Goal: Connect Sell Button to backend POST /sell API route
            if st.button("📉 Execute Sell Order", use_container_width=True):
                res = requests.post(f"{BACKEND_URL}/sell?username=trader1&ticker={clean_ticker}&shares={shares_sell}")
                if res.status_code == 200:
                    st.success(f"Successfully sold {shares_sell} shares of {clean_ticker}!")
                    st.rerun()
                else:
                    st.error(f"Error: {res.json()['detail']}")
    else:
        st.error("Invalid ticker asset symbol or no market data found.")

# --- PAGE 3: TRANSACTION HISTORY ---
elif page == "📜 Transaction History":
    st.title("📜 Complete Account Transaction Ledger")
    
    # Fetch full history directly from the profile endpoint
    try:
        res = requests.get(f"{BACKEND_URL}/user/trader1")
        if res.status_code == 200 and res.json().get("ledger"):
            df_ledger = pd.DataFrame(res.json()["ledger"])
            st.dataframe(df_ledger, use_container_width=True)
        else:
            st.info("No transactional ledger records logged on this account profile yet.")
    except Exception:
        st.error("Could not fetch ledger logs from the backend database server.")