from sqlalchemy import create_engine, text

DB_PATH = "/home/ubuntu/projects/tradingbot/database/tradingbot.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = result.fetchall()
    print("Tables:", tables)
