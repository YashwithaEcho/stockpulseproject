from fastapi import FastAPI, HTTPException
from data_fetcher import fetch_stock_history

# Initialize the FastAPI application instance
app = FastAPI(title="StockPulse Backend API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the StockPulse Backend API Terminal!"}

# Days 5-7 Goal: Create a GET endpoint that returns live data as JSON
@app.get("/price/{ticker}")
def get_stock_price(ticker: str):
    """
    Fetches the latest market closing price for a given stock ticker symbol.
    """
    # Standardize the symbol string
    clean_ticker = ticker.upper().strip()
    
    # Use your Day 2 fetching logic (requesting 1 month of recent data)
    df = fetch_stock_history(clean_ticker, timeframe="1mo")
    
    # Error checking: If no data returned or dataframe is empty, trigger a 404
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"Ticker '{clean_ticker}' not found or no data available.")
    
    # Extract the very last row's closing price
    latest_close = float(df['Close'].iloc[-1])
    latest_date = str(df.index[-1])
    
    # Return a clean JSON key-value response structure
    return {
        "ticker": clean_ticker,
        "latest_price": round(latest_close, 2),
        "as_of_date": latest_date
    }