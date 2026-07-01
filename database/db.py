# db.py
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_DIR = os.path.join(BASE_DIR, "archive", "database-snapshots")

def financial_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "financial.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def trading_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "tradingbot.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def conversation_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "conversation.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def settings_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "settings.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def logs_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "logs.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def research_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "research.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def news_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "news.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def portfolio_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(SNAPSHOT_DIR, "portfolio.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# just create db
# if __name__ == "__main__":

#     conversation_db()

#     logs_db()
#     research_db()
#     news_db()
#     portfolio_db()

#     print("Database connections created successfully.")
