import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_NAME = os.getenv("MONGO_NAME", "autoluno")

_client = None


def mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def mongo_db():
    return mongo_client()[MONGO_NAME]


def now_utc():
    return datetime.now(timezone.utc)


def ensure_indexes():
    db = mongo_db()
    db.ticker_history.create_index([("pair", ASCENDING), ("raw_timestamp", ASCENDING)])
    db.balance_history.create_index([("asset", ASCENDING), ("timestamp", ASCENDING)])
    db.trade_history.create_index([("pair", ASCENDING), ("sequence", ASCENDING)])
    db.fee_history.create_index([("pair", ASCENDING), ("timestamp", ASCENDING)])
    db.market_history.create_index([("pair", ASCENDING), ("timestamp", ASCENDING)])
    db.pairs_list.create_index("pairs", unique=True)
    db.assets_list.create_index("assets", unique=True)
    db.app_settings.create_index("key", unique=True)
    db.audi_bot_settings.create_index("pair", unique=True)
    db.bot_decision_log.create_index([("pair", ASCENDING), ("createdAt", ASCENDING)])


def insert_many(collection_name, documents):
    docs = list(documents)
    if not docs:
        return 0
    ensure_indexes()
    mongo_db()[collection_name].insert_many(docs)
    return len(docs)


def upsert_unique(collection_name, key, value, document):
    ensure_indexes()
    mongo_db()[collection_name].update_one(
        {key: value},
        {"$setOnInsert": document},
        upsert=True,
    )


def list_collection(collection_name, sort=None):
    ensure_indexes()
    cursor = mongo_db()[collection_name].find({}, {"_id": False})
    if sort:
        cursor = cursor.sort(sort)
    return list(cursor)


def grouped_history(collection_name, group_key):
    rows = list_collection(collection_name)
    grouped = {}
    for row in rows:
        key = row.get(group_key)
        if key is None:
            continue
        grouped.setdefault(key, {group_key: key, "history": []})["history"].append(row)
    return list(grouped.values())


def get_setting(key, default=None):
    ensure_indexes()
    row = mongo_db().app_settings.find_one({"key": key}, {"_id": False})
    if row:
        return row.get("value", default)
    return default


def set_setting(key, value):
    ensure_indexes()
    mongo_db().app_settings.update_one(
        {"key": key},
        {"$set": {"key": key, "value": value, "updatedAt": now_utc()}},
        upsert=True,
    )
