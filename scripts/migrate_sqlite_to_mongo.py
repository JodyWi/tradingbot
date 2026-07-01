#!/usr/bin/env python3
from pathlib import Path
import sqlite3
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database.mongo import mongo_db, set_setting

DATABASE_DIR = ROOT / "database"

FINANCIAL_TABLES = [
    "ticker_history",
    "balance_history",
    "trade_history",
    "fee_history",
    "market_history",
    "pairs_list",
    "assets_list",
]


def read_rows(db_path, table):
    if not db_path.exists():
        return []
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table}")]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def migrate_collection(sqlite_db, table, collection):
    rows = read_rows(sqlite_db, table)
    if not rows:
        print(f"{table}: no rows")
        return
    for row in rows:
        row["legacySqliteId"] = row.pop("id", None)
        row["legacySource"] = sqlite_db.name
    collection.insert_many(rows)
    print(f"{table}: migrated {len(rows)} rows")


def migrate_settings():
    settings_db = DATABASE_DIR / "settings.db"
    mappings = [
        ("feesinfo_settings", "feesinfo"),
        ("marketsinfo_settings", "marketsinfo"),
        ("tradesinfo_settings", "tradesinfo"),
    ]
    for table, key in mappings:
        rows = read_rows(settings_db, table)
        if not rows:
            print(f"{table}: no rows")
            continue
        row = rows[0]
        set_setting(key, {
            "autoFetch": bool(row.get("autoFetch")),
            "autoFetchTime": row.get("autoFetchTime") or "23:00",
        })
        print(f"{table}: migrated singleton setting")

    audi_rows = read_rows(settings_db, "audi_bot_settings")
    if audi_rows:
        collection = mongo_db().audi_bot_settings
        for row in audi_rows:
            row["legacySqliteId"] = row.pop("id", None)
            row["legacySource"] = settings_db.name
            collection.update_one(
                {"pair": row.get("pair")},
                {"$set": row},
                upsert=True,
            )
        print(f"audi_bot_settings: migrated {len(audi_rows)} rows")
    else:
        print("audi_bot_settings: no rows")


def main():
    financial_db = DATABASE_DIR / "financial.db"
    db = mongo_db()
    for table in FINANCIAL_TABLES:
        migrate_collection(financial_db, table, db[table])
    migrate_settings()


if __name__ == "__main__":
    main()
