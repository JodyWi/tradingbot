#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json
import sqlite3
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database.mongo import ensure_indexes, mongo_db, set_setting

SNAPSHOT_DIR = ROOT / "archive" / "database-snapshots"

ACTIVE_FINANCIAL_TABLES = [
    "ticker_history",
    "balance_history",
    "trade_history",
    "fee_history",
    "market_history",
    "pairs_list",
    "assets_list",
]

SETTINGS_TABLES = {
    "feesinfo_settings": "feesinfo",
    "marketsinfo_settings": "marketsinfo",
    "tradesinfo_settings": "tradesinfo",
}


def table_names(db_path):
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return [row[0] for row in rows if row[0] != "sqlite_sequence"]


def read_rows(db_path, table):
    if not db_path.exists():
        return []
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(f'SELECT * FROM "{table}"')]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def migrated_document(row, sqlite_db, table):
    doc = dict(row)
    legacy_id = doc.pop("id", None)
    doc["legacySqliteId"] = legacy_id
    doc["legacySource"] = sqlite_db.name
    doc["legacyTable"] = table
    return doc


def migration_filter(doc):
    if doc.get("uid"):
        return {
            "legacySource": doc["legacySource"],
            "legacyTable": doc["legacyTable"],
            "uid": doc["uid"],
        }
    return {
        "legacySource": doc["legacySource"],
        "legacyTable": doc["legacyTable"],
        "legacySqliteId": doc.get("legacySqliteId"),
    }


def upsert_rows(collection, rows, sqlite_db, table):
    count = 0
    for row in rows:
        doc = migrated_document(row, sqlite_db, table)
        collection.update_one(
            migration_filter(doc),
            {"$set": doc},
            upsert=True,
        )
        count += 1
    return count


def migrate_active_financial():
    financial_db = SNAPSHOT_DIR / "financial.db"
    db = mongo_db()
    summary = {}
    for table in ACTIVE_FINANCIAL_TABLES:
        rows = read_rows(financial_db, table)
        if not rows:
            print(f"active {table}: no rows")
            summary[table] = 0
            continue
        migrated = upsert_rows(db[table], rows, financial_db, table)
        print(f"active {table}: migrated {migrated} rows")
        summary[table] = migrated
    return summary


def migrate_settings():
    settings_db = SNAPSHOT_DIR / "settings.db"
    summary = {}
    for table, key in SETTINGS_TABLES.items():
        rows = read_rows(settings_db, table)
        if not rows:
            print(f"{table}: no rows")
            summary[table] = 0
            continue
        row = rows[0]
        set_setting(
            key,
            {
                "autoFetch": bool(row.get("autoFetch")),
                "autoFetchTime": row.get("autoFetchTime") or "23:00",
            },
        )
        print(f"{table}: migrated singleton setting")
        summary[table] = 1

    audi_rows = read_rows(settings_db, "audi_bot_settings")
    collection = mongo_db().audi_bot_settings
    migrated = 0
    for row in audi_rows:
        doc = migrated_document(row, settings_db, "audi_bot_settings")
        collection.update_one(
            {"pair": doc.get("pair")},
            {"$set": doc},
            upsert=True,
        )
        migrated += 1
    print(f"audi_bot_settings: migrated {migrated} rows")
    summary["audi_bot_settings"] = migrated
    return summary


def migrate_sqlite_snapshots():
    db = mongo_db()
    summary = {}
    for sqlite_db in sorted(SNAPSHOT_DIR.glob("*.db")):
        for table in table_names(sqlite_db):
            rows = read_rows(sqlite_db, table)
            collection_name = f"legacy_{sqlite_db.stem}_{table}"
            migrated = upsert_rows(db[collection_name], rows, sqlite_db, table)
            print(f"{collection_name}: migrated {migrated} rows")
            summary[collection_name] = migrated
    return summary


def migrate_json_snapshots():
    db = mongo_db()
    summary = {}
    for json_path in sorted((SNAPSHOT_DIR / "data").glob("*.json")):
        collection_name = f"legacy_json_{json_path.stem}"
        rows = json.loads(json_path.read_text())
        if isinstance(rows, dict):
            rows = [rows]
        migrated = 0
        for row in rows:
            doc = dict(row)
            legacy_id = doc.pop("id", None)
            doc["legacyJsonId"] = legacy_id
            doc["legacySource"] = f"database/data/{json_path.name}"
            db[collection_name].update_one(
                {
                    "legacySource": doc["legacySource"],
                    "legacyJsonId": doc.get("legacyJsonId"),
                },
                {"$set": doc},
                upsert=True,
            )
            migrated += 1
        print(f"{collection_name}: migrated {migrated} rows")
        summary[collection_name] = migrated
    return summary


def write_manifest(summary):
    mongo_db().migration_runs.insert_one(
        {
            "name": "sqlite_to_mongo",
            "source": str(SNAPSHOT_DIR.relative_to(ROOT)),
            "ranAt": datetime.now(timezone.utc),
            "summary": summary,
        }
    )


def main():
    ensure_indexes()
    summary = {
        "active_financial": migrate_active_financial(),
        "settings": migrate_settings(),
        "sqlite_snapshots": migrate_sqlite_snapshots(),
        "json_snapshots": migrate_json_snapshots(),
    }
    write_manifest(summary)


if __name__ == "__main__":
    main()
