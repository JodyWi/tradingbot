# audi_bot/utils.py

from database.db import settings_db  # ✅ Use your helper!
import uuid

def ensure_table():
    """Ensure the settings table exists with UID and auto-increment ID"""
    with settings_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audi_bot_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                pair TEXT UNIQUE,
                maxTradeSize REAL,
                riskLevel TEXT
            );
        """)
    print("[Audi Bot] Settings table ensured.")


def save_settings(pair, max_trade_size, risk_level):
    """Save or update settings with UID"""
    ensure_table()
    with settings_db() as conn:
        # Try get existing UID for pair
        row = conn.execute(
            "SELECT uid FROM audi_bot_settings WHERE pair = ?",
            (pair,)
        ).fetchone()
        uid = row[0] if row else str(uuid.uuid4())

        conn.execute("""
            INSERT OR REPLACE INTO audi_bot_settings (
                id, uid, pair, maxTradeSize, riskLevel
            )
            VALUES (
                COALESCE((SELECT id FROM audi_bot_settings WHERE pair = ?), NULL),
                ?, ?, ?, ?
            )
        """, (
            pair,
            uid,
            pair,
            max_trade_size,
            risk_level
        ))
    print(f"[Audi Bot] Saved settings for {pair} (UID: {uid})")


def get_settings(pair=None):
    ensure_table()
    with settings_db() as conn:
        if pair:
            cursor = conn.execute(
                "SELECT pair, maxTradeSize, riskLevel FROM audi_bot_settings WHERE pair = ?",
                (pair,)
            )
            row = cursor.fetchone()
            if row:
                return dict(zip(["pair", "maxTradeSize", "riskLevel"], row))
            return {}
        else:
            # fallback: get all
            cursor = conn.execute(
                "SELECT pair, maxTradeSize, riskLevel FROM audi_bot_settings"
            )
            rows = [dict(zip(["pair", "maxTradeSize", "riskLevel"], row)) for row in cursor.fetchall()]
            return rows


def get_settings_for_pair(pair):
    with settings_db() as conn:
        cursor = conn.execute(
            "SELECT pair, maxTradeSize, riskLevel FROM audi_bot_settings WHERE pair = ?",
            (pair,)
        )
        row = cursor.fetchone()
        if row:
            return dict(zip(["pair", "maxTradeSize", "riskLevel"], row))
    return {}



def delete_settings_by_pair(pair):
    ensure_table()
    with settings_db() as conn:
        conn.execute("""
            DELETE FROM audi_bot_settings
            WHERE pair = ?
        """, (pair,))
    print(f"[Audi Bot] Deleted settings for {pair}")