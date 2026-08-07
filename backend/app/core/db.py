"""Injectable required MongoDB boundary with compatibility helpers."""

from datetime import datetime, timezone
from typing import Any, Protocol

from pymongo import ASCENDING, MongoClient

from .config import Settings


class PrimaryDatabase(Protocol):
    def status(self) -> dict[str, Any]: ...
    def collection(self, name: str) -> Any: ...
    def raw(self) -> Any: ...
    def close(self) -> None: ...


class MongoPrimaryDatabase:
    def __init__(self, settings: Settings, *, client: Any | None = None) -> None:
        self.settings = settings.validate()
        self.client = client or MongoClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=int(settings.mongo_timeout_seconds * 1000),
            connectTimeoutMS=int(settings.mongo_timeout_seconds * 1000),
        )
        self.database = self.client[settings.mongo_database]

    def status(self) -> dict[str, Any]:
        try:
            self.client.admin.command("ping")
            return {"required": True, "backend": "mongodb", "state": "healthy", "ok": True}
        except Exception as exc:
            return {"required": True, "backend": "mongodb", "state": "unavailable",
                    "ok": False, "error": type(exc).__name__}

    def collection(self, name: str) -> Any:
        return self.database[name]

    def raw(self) -> Any:
        return self.database

    def close(self) -> None:
        self.client.close()


_database: PrimaryDatabase | None = None


def configure_database(database: PrimaryDatabase) -> None:
    global _database
    _database = database


def database_service() -> PrimaryDatabase:
    global _database
    if _database is None:
        _database = MongoPrimaryDatabase(Settings.from_env())
    return _database


def mongo_client():
    return getattr(database_service(), "client", None)


def mongo_db():
    return database_service().raw()


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
    db.audit_events.create_index([("timestamp", ASCENDING)])


def insert_many(collection_name, documents):
    docs = list(documents)
    if not docs:
        return 0
    ensure_indexes()
    mongo_db()[collection_name].insert_many(docs)
    return len(docs)


def upsert_unique(collection_name, key, value, document):
    ensure_indexes()
    mongo_db()[collection_name].update_one({key: value}, {"$setOnInsert": document}, upsert=True)


def list_collection(collection_name, sort=None):
    ensure_indexes()
    cursor = mongo_db()[collection_name].find({}, {"_id": False})
    return list(cursor.sort(sort) if sort else cursor)


def grouped_history(collection_name, group_key):
    grouped = {}
    for row in list_collection(collection_name):
        key = row.get(group_key)
        if key is not None:
            grouped.setdefault(key, {group_key: key, "history": []})["history"].append(row)
    return list(grouped.values())


def get_setting(key, default=None):
    ensure_indexes()
    row = mongo_db().app_settings.find_one({"key": key}, {"_id": False})
    return row.get("value", default) if row else default


def set_setting(key, value):
    ensure_indexes()
    mongo_db().app_settings.update_one(
        {"key": key}, {"$set": {"key": key, "value": value, "updatedAt": now_utc()}}, upsert=True
    )
