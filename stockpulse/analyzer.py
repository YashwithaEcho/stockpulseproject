import pandas as pd
from data_fetcher import fetch_stock_history

def calculate_indicators(df):
    """
    Takes a stock dataframe and adds technical indicators: Daily Returns and 5-day SMA.
    """
    if df is None or df.empty:
        return None
    
    # Create a clean copy to avoid warnings
    analysis_df = df.copy()
    
    # 1. Calculate Daily Return percentage
    # formula: ((Current Close - Previous Close) / Previous Close) * 100
    analysis_df['Daily_Return_%'] = analysis_df['Close'].pct_change() * 100
    
    # 2. Calculate 5-Day Simple Moving Average (SMA)
    # Averaging the closing prices over a rolling 5-day window
    analysis_df['5_Day_SMA'] = analysis_df['Close'].rolling(window=5).mean()
    
    return analysis_df

if __name__ == "__main__":
    ticker = "AAPL"
    # Fetch 1 month of historical data using our Day 2 engine
    raw_data = fetch_stock_history(ticker, timeframe="1mo")
    
    if raw_data is not None:
        print("\n⚙️ Processing data and calculating trading indicators...")
        processed_data = calculate_indicators(raw_data)
        
        print("\n📊 Done! Here are the latest insights for your dashboard:")
        # Display the core data along with our new calculated columns
        display_columns = ['Close', 'Daily_Return_%', '5_Day_SMA']
        print(processed_data[display_columns].tail())