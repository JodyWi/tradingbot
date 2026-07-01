# database/settings.py
from database.db import settings_db

import uuid



# def ensure_table(val1, val2, val3):




# feesinfo_settings - Field or collection name
# autoFetch - boolen
# autoFetchTime - int dont know how to store time lol
def create_feesinfo_settings_table():
    conn = settings_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feesinfo_settings (
            id TEXT PRIMARY KEY,
            autoFetch INTEGER NOT NULL DEFAULT 0,
            autoFetchTime TEXT NOT NULL DEFAULT '23:00'
        )
    """)
    conn.commit()
    conn.close()

    
def upsert_feesinfo_settings(autoFetch: bool, autoFetchTime: str):
    create_feesinfo_settings_table()
    conn = settings_db()   # ✅ get the connection object
    cursor = conn.cursor()

    id = "singleton"
    existing = cursor.execute(
        "SELECT id FROM feesinfo_settings WHERE id = ?",
        (id,)
    ).fetchone()

    if existing:
        cursor.execute(
            "UPDATE feesinfo_settings SET autoFetch = ?, autoFetchTime = ? WHERE id = ?",
            (int(autoFetch), autoFetchTime, id)
        )
    else:
        cursor.execute(
            "INSERT INTO feesinfo_settings (id, autoFetch, autoFetchTime) VALUES (?, ?, ?)",
            (id, int(autoFetch), autoFetchTime)
        )

    conn.commit()
    conn.close()


def get_feesinfo_settings():
    create_feesinfo_settings_table()
    with settings_db() as conn:
        row = conn.execute(
            "SELECT autoFetch, autoFetchTime FROM feesinfo_settings WHERE id = ?",
            ("singleton",),
        ).fetchone()
    if row:
        return {"autoFetch": bool(row[0]), "autoFetchTime": row[1]}
    return {"autoFetch": False, "autoFetchTime": "23:00"}

#################################################################

def create_marketsinfo_settings_table():
    conn = settings_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketsinfo_settings (
            id TEXT PRIMARY KEY,
            autoFetch INTEGER NOT NULL DEFAULT 0,
            autoFetchTime TEXT NOT NULL DEFAULT '23:00'
        )
    """)
    conn.commit()
    conn.close()

def upsert_marketsinfo_settings(autoFetch: bool, autoFetchTime: str):
    create_marketsinfo_settings_table()
    conn = settings_db()   # ✅ get the connection object
    cursor = conn.cursor()

    id = "singleton"
    existing = cursor.execute(
        "SELECT id FROM marketsinfo_settings WHERE id = ?",
        (id,)
    ).fetchone()

    if existing:
        cursor.execute(
            "UPDATE marketsinfo_settings SET autoFetch = ?, autoFetchTime = ? WHERE id = ?",
            (int(autoFetch), autoFetchTime, id)
        )
    else:
        cursor.execute(
            "INSERT INTO marketsinfo_settings (id, autoFetch, autoFetchTime) VALUES (?, ?, ?)",
            (id, int(autoFetch), autoFetchTime)
        )

    conn.commit()
    conn.close()


def get_marketsinfo_settings():
    create_marketsinfo_settings_table()
    with settings_db() as conn:
        row = conn.execute(
            "SELECT autoFetch, autoFetchTime FROM marketsinfo_settings WHERE id = ?",
            ("singleton",),
        ).fetchone()
    if row:
        return {"autoFetch": bool(row[0]), "autoFetchTime": row[1]}
    return {"autoFetch": False, "autoFetchTime": "23:00"}

#################################################################

def create_tradesinfo_settings_table():
    conn = settings_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tradesinfo_settings (
            id TEXT PRIMARY KEY,
            autoFetch INTEGER NOT NULL DEFAULT 0,
            autoFetchTime TEXT NOT NULL DEFAULT '23:00'
        )
    """)
    conn.commit()
    conn.close()


def upsert_tradesinfo_settings(autoFetch: bool, autoFetchTime: str):
    create_tradesinfo_settings_table()
    conn = settings_db()
    cursor = conn.cursor()

    id = "singleton"
    existing = cursor.execute(
        "SELECT id FROM tradesinfo_settings WHERE id = ?",
        (id,)
    ).fetchone()

    if existing:
        cursor.execute(
            "UPDATE tradesinfo_settings SET autoFetch = ?, autoFetchTime = ? WHERE id = ?",
            (int(autoFetch), autoFetchTime, id)
        )
    else:
        cursor.execute(
            "INSERT INTO tradesinfo_settings (id, autoFetch, autoFetchTime) VALUES (?, ?, ?)",
            (id, int(autoFetch), autoFetchTime)
        )

    conn.commit()
    conn.close()


def get_tradesinfo_settings():
    create_tradesinfo_settings_table()
    with settings_db() as conn:
        row = conn.execute(
            "SELECT autoFetch, autoFetchTime FROM tradesinfo_settings WHERE id = ?",
            ("singleton",),
        ).fetchone()
    if row:
        return {"autoFetch": bool(row[0]), "autoFetchTime": row[1]}
    return {"autoFetch": False, "autoFetchTime": "23:00"}
