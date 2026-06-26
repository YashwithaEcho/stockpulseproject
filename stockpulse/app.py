import streamlit as st

# Set up page styling configuration
st.set_page_config(page_title="StockPulse Dashboard", layout="wide")

# --- SIDEBAR NAVIGATION (Days 3-5 Goal) ---
st.sidebar.title("🎛️ Navigation Panel")
page = st.sidebar.radio(
    "Go To Page:", 
    ["📊 Dashboard", "🔍 Search & Trade", "📜 Transaction History"]
)

# Mock data for Week 3 UI rendering (We will wire this to the database in Week 4)
mock_cash = 10000.00
mock_net_worth = 12450.75

# --- PAGE 1: DASHBOARD ---
if page == "📊 Dashboard":
    st.title("📈 StockPulse Market Analytics Dashboard")
    st.markdown("Welcome back, **trader1**! Here is your current financial standing:")
    
    # Days 1-2 Goal: Metric card showing wallet balance
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="💰 Virtual Cash Balance", value=f"${mock_cash:,.2f}")
    with col2:
        st.metric(label="📊 Total Portfolio Net Worth", value=f"${mock_net_worth:,.2f}")
        
    st.info("💡 Tip: Use the navigation menu on the left side to look up active live stock symbols or view historical logs.")

# --- PAGE 2: SEARCH & TRADE ---
elif page == "🔍 Search & Trade":
    st.title("💱 Live Asset Trading Desk")
    
    # Days 3-5 Goal: st.text_input search box
    ticker_input = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA, NVDA):", "AAPL")
    clean_ticker = ticker_input.upper().strip()
    
    st.subheader(f"Trading Actions for {clean_ticker}")
    
    col1, col2 = st.columns(2)
    with col1:
        shares_buy = st.number_input("Shares to Buy", min_value=1, value=1, step=1)
        if st.button("🚀 Execute Buy Order", use_container_width=True):
            st.warning("Backend engine connection coming in Week 4!")
            
    with col2:
        shares_sell = st.number_input("Shares to Sell", min_value=1, value=1, step=1)
        if st.button("📉 Execute Sell Order", use_container_width=True):
            st.warning("Backend engine connection coming in Week 4!")

# --- PAGE 3: TRANSACTION HISTORY ---
elif page == "📜 Transaction History":
    st.title("📜 Account Transaction History Log")
    st.markdown("Review your historical buy and sell ledger actions below:")
    
    # Placeholders for Week 4 database fetching
    st.write("No transaction records found for this trade session yet.")