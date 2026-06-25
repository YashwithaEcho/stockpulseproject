import yfinance as yf

def get_stock_price(ticker_symbol):
    # Fetch the stock data from Yahoo Finance
    ticker_data = yf.Ticker(ticker_symbol)
    
    # Get the latest price information
    todays_data = ticker_data.history(period='1d')
    
    # Safe check: if yfinance returns a tuple, grab the first element (the DataFrame)
    if isinstance(todays_data, tuple):
        todays_data = todays_data[0]
        
    # Extract the actual closing price cleanly using .iloc or .values
    latest_price = todays_data['Close'].iloc[-1]
    return round(latest_price, 2)

# Test it out with Apple
symbol = "AAPL"
current_price = get_stock_price(symbol)

print("-" * 40)
print(f"Success! The live price of {symbol} is: ${current_price}")
print("-" * 40)