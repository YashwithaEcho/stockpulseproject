from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# Create a database engine pointing to a local file named 'stockpulse.db'
DATABASE_URL = "sqlite:///./stockpulse.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- TABLE 1: USERS ---
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    balance = Column(Float, default=10000.0)  # Starting mock cash balance

# --- TABLE 2: TRANSACTIONS ---
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String, index=True)
    shares = Column(Integer)
    price = Column(Float)
    type = Column(String)  # Will be 'BUY' or 'SELL'

# Simple helper function to automatically generate the database tables
def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Let's seed a default testing user if the database is brand new
    db = SessionLocal()
    if not db.query(User).filter(User.username == "trader1").first():
        test_user = User(username="trader1", balance=10000.0)
        db.add(test_user)
        db.commit()
    db.close()

if __name__ == "__main__":
    print("🗄️ Initializing SQLite database and building tables...")
    init_db()
    print("✅ Database tables initialized successfully!")