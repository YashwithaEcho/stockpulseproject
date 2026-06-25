import streamlit as str
import pandas as pd
from data_fetcher import fetch_stock_history
from analyzer import calculate_indicators

# Set page style configuration
str.set_page_config(page_title="StockPulse Dashboard", layout="wide")

str.title("📈 StockPulse: Live Market Analytics Dashboard")
str.markdown("Welcome to your personal market data terminal.")

# --- SIDEBAR CONTROL PANEL ---
str.sidebar.header("🕹️ Control Panel")
user_ticker = str.sidebar.text_input("Enter Stock Ticker Symbol:", value="AAPL").upper().strip()
time_window = str.sidebar.selectbox("Select Timeframe:", options=["1mo", "3mo", "6mo", "1y"])

# --- DATA PROCESSING LINK ---
if user_ticker:
    raw_df = fetch_stock_history(user_ticker, timeframe=time_window)
    
    if raw_df is not None and not raw_df.empty:
        # Pass the data to your calculation engine
        analyzed_df = calculate_indicators(raw_df)
        
        # Display key metrics side-by-side
        latest_row = analyzed_df.iloc[-1]
        latest_price = round(latest_row['Close'], 2)
        latest_return = round(latest_row['Daily_Return_%'], 2)
        
        col1, col2 = str.columns(2)
        col1.metric("Current Price", f"${latest_price}")
        col2.metric("Daily Change", f"{latest_return}%", delta=f"{latest_return}%")
        
        # --- CHARTS SECTION ---
        str.subheader(f"📊 Closing Price & 5-Day Trend for {user_ticker}")
        # Charting the closing price and the simple moving average trend line
        str.line_chart(analyzed_df[['Close', '5_Day_SMA']])
        
        # --- DATA ROWS SECTION ---
        str.subheader("📋 Recent Analytics Data Log")
        str.dataframe(analyzed_df[['Close', 'Daily_Return_%', '5_Day_SMA']].tail(10))
        
    else:
        str.error("Could not fetch data for that symbol. Please type a valid stock ticker.")