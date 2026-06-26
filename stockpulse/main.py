from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from data_fetcher import fetch_stock_history
from models import SessionLocal, User, Transaction, init_db

# Automatically verify database tables exist on server startup
init_db()

app = FastAPI(title="StockPulse Advanced Transaction Terminal")

# Dependency helper tool to securely open and close database connections per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "Online", "message": "Transaction Engine Active"}

# --- GET PRICE ---
@app.get("/price/{ticker}")
def get_stock_price(ticker: str):
    clean_ticker = ticker.upper().strip()
    df = fetch_stock_history(clean_ticker, timeframe="1mo")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    return {"ticker": clean_ticker, "latest_price": round(float(df['Close'].iloc[-1]), 2)}

# --- BUY STOCK ---
@app.post("/buy")
def buy_stock(username: str, ticker: str, shares: int, db: Session = Depends(get_db)):
    clean_ticker = ticker.upper().strip()
    if shares <= 0:
        raise HTTPException(status_code=400, detail="Share quantity must be greater than 0.")
        
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")
        
    df = fetch_stock_history(clean_ticker, timeframe="1mo")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"Could not verify price for asset symbol '{clean_ticker}'.")
    
    current_price = round(float(df['Close'].iloc[-1]), 2)
    total_cost = current_price * shares
    
    if user.balance < total_cost:
        raise HTTPException(status_code=400, detail=f"Insufficient funds. Balance: ${user.balance:.2f}")
        
    user.balance -= total_cost
    new_transaction = Transaction(user_id=user.id, ticker=clean_ticker, shares=shares, price=current_price, type="BUY")
    
    db.add(new_transaction)
    db.commit()
    db.refresh(user)
    return {"message": "Purchase Successful!", "remaining_cash_balance": round(user.balance, 2)}

# --- WEEK 2 DAYS 6-7: SELL STOCK ENDPOINT ---
@app.post("/sell")
def sell_stock(username: str, ticker: str, shares: int, db: Session = Depends(get_db)):
    """
    Executes a stock sell transaction: Checks if the user owns enough shares,
    calculates proceeds at market price, adds cash back to balance, and logs to ledger.
    """
    clean_ticker = ticker.upper().strip()
    if shares <= 0:
        raise HTTPException(status_code=400, detail="Share quantity must be greater than 0.")
        
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    # Calculate how many shares the user actually owns right now
    history = db.query(Transaction).filter(Transaction.user_id == user.id, Transaction.ticker == clean_ticker).all()
    owned_shares = 0
    for tx in history:
        if tx.type == "BUY":
            owned_shares += tx.shares
        elif tx.type == "SELL":
            owned_shares -= tx.shares
            
    if owned_shares < shares:
        raise HTTPException(status_code=400, detail=f"You only own {owned_shares} shares of {clean_ticker}. Cannot sell {shares}.")
        
    df = fetch_stock_history(clean_ticker, timeframe="1mo")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="Could not retrieve current market price.")
        
    current_price = round(float(df['Close'].iloc[-1]), 2)
    sale_proceeds = current_price * shares
    
    # Credit cash back to user account balance
    user.balance += sale_proceeds
    new_transaction = Transaction(user_id=user.id, ticker=clean_ticker, shares=shares, price=current_price, type="SELL")
    
    db.add(new_transaction)
    db.commit()
    db.refresh(user)
    return {"message": "Sale Successful!", "added_cash": sale_proceeds, "new_cash_balance": round(user.balance, 2)}

# --- WEEK 2 DAYS 6-7: USER PROFILE & PORTFOLIO VALUATION ---
@app.get("/user/{username}")
def get_user_profile(username: str, db: Session = Depends(get_db)):
    """
    Returns user balance and calculates total current portfolio valuation 
    by looking up live prices for all holdings.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    history = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    
    # Aggregate net holdings per stock ticker
    holdings = {}
    for tx in history:
        if tx.ticker not in holdings:
            holdings[tx.ticker] = 0
        if tx.type == "BUY":
            holdings[tx.ticker] += tx.shares
        elif tx.type == "SELL":
            holdings[tx.ticker] -= tx.shares

    # Calculate current value of holdings based on live pricing
    portfolio_value = 0.0
    holdings_summary = []
    
    for ticker, shares_count in holdings.items():
        if shares_count > 0:
            df = fetch_stock_history(ticker, timeframe="1mo")
            current_price = round(float(df['Close'].iloc[-1]), 2) if (df is not None and not df.empty) else 0.0
            asset_value = current_price * shares_count
            portfolio_value += asset_value
            holdings_summary.append({
                "ticker": ticker,
                "shares_owned": shares_count,
                "current_price": current_price,
                "total_value": round(asset_value, 2)
            })
            
    return {
        "username": user.username,
        "cash_balance": round(user.balance, 2),
        "portfolio_holdings_value": round(portfolio_value, 2),
        "total_net_worth": round(user.balance + portfolio_value, 2),
        "current_holdings": holdings_summary
    }