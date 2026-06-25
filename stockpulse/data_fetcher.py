import yfinance as yf
import pandas as pd

def fetch_stock_history(ticker_symbol, timeframe="1mo"):
    """
    Fetches historical stock data for a given ticker and timeframe.
    Timeframe options: '1d', '5d', '1mo', '3mo', '6mo', '1y', 'max'
    """
    print(f"\n🔄 Connecting to market data for: {ticker_symbol} ({timeframe})...")
    
    try:
        # Initialize the ticker object
        stock = yf.Ticker(ticker_symbol)
        
        # Fetch historical data
        historical_df = stock.history(period=timeframe)
        
        # If the returned data is empty, the ticker probably doesn't exist
        if historical_df.empty:
            print(f"❌ Error: No data found for ticker '{ticker_symbol}'. Please check the symbol.")
            return None
            
        return historical_df

    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")
        return None

# --- TEST EXECUTIONS ---
if __name__ == "__main__":
    # Test 1: Fetching valid data (Apple for 1 month)
    ticker = "AAPL"
    data = fetch_stock_history(ticker, timeframe="1mo")
    
    if data is not None:
        print(f"✅ Success! Retrieved {len(data)} days of data.")
        print("\n📊 Here is a sneak peek at the last 5 days of market data:")
        # Displaying just the main columns to keep it clean
        print(data[['Open', 'High', 'Low', 'Close', 'Volume']].tail())
        
    print("-" * 50)
    
    # Test 2: Testing our error handler with a fake ticker
    fake_ticker = "XYZ_INVALID"
    fetch_stock_history(fake_ticker)