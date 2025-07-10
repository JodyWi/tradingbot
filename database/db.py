# db.py
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def financial_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "financial.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def trading_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "tradingbot.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def conversation_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "conversation.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def settings_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "settings.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def logs_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "logs.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def research_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "research.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def news_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "news.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def portfolio_db():
    """Local DB connection just for this script"""
    DB_PATH = os.path.join(BASE_DIR, "database", "portfolio.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# just create db
# if __name__ == "__main__":

#     conversation_db()

#     logs_db()
#     research_db()
#     news_db()
#     portfolio_db()

#     print("Database connections created successfully.")