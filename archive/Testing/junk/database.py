import sqlite3
import os

# Define database path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "tradingbot.db")

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def connect_db():
    """Connect to SQLite database, creating it if it doesn't exist."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    """Create necessary tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # ✅ Create Trades Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            asset TEXT NOT NULL,
            trade_type TEXT NOT NULL,  -- 'BUY' or 'SELL'
            amount REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # ✅ Create Balances Table (with UNIQUE constraint)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            asset TEXT NOT NULL UNIQUE,  -- Unique constraint for conflict handling
            balance REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Database and tables created successfully at {DB_PATH}")

# ✅ Insert New Trade
def insert_trade(asset, trade_type, amount, price):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trades (asset, trade_type, amount, price)
            VALUES (?, ?, ?, ?)
        ''', (asset, trade_type, float(amount), float(price)))  # Convert to float
        conn.commit()
        print(f"✅ Trade recorded: {asset} {trade_type} {amount} @ {price}")
    except Exception as e:
        print(f"❌ Error inserting trade: {e}")
    finally:
        conn.close()

# ✅ Insert or Update Balance
def update_balance(asset, balance):
    try:
        balance = float(balance)  # Ensure it's a valid float
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO balances (asset, balance) 
            VALUES (?, ?)
            ON CONFLICT(asset) DO UPDATE SET balance = excluded.balance
        ''', (asset, balance))
        conn.commit()
        print(f"✅ Balance updated: {asset} => {balance}")
    except Exception as e:
        print(f"❌ Error updating balance: {e}")
    finally:
        conn.close()

# ✅ Retrieve All Trades
def get_all_trades():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC")
    trades = cursor.fetchall()
    conn.close()
    return trades

# ✅ Retrieve Balance for a Specific Asset
def get_balance(asset):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM balances WHERE asset = ?", (asset,))
    balance = cursor.fetchone()
    conn.close()
    return float(balance[0]) if balance else None  # Ensure float return

# ✅ For Initial Database Setup
if __name__ == "__main__":
    create_tables()
