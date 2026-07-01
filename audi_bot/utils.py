from database.mongo import mongo_db, now_utc

DEFAULT_BOT_SETTINGS = {
    "strategyEnabled": False,
    "strategyIntervalMinutes": 5,
    "model": "qwen2.5-coder:0.5b",
    "ollamaUrl": "http://127.0.0.1:11434",
    "maxPaperTradeSize": 100.0,
    "minDecisionIntervalMinutes": 5,
    "maxDecisionsPerHour": 12,
}


def ensure_table():
    """Compatibility shim for older callers; Mongo indexes are created lazily."""
    mongo_db().audi_bot_settings.create_index("pair", unique=True)


def save_settings(pair, max_trade_size, risk_level):
    ensure_table()
    mongo_db().audi_bot_settings.update_one(
        {"pair": pair},
        {
            "$set": {
                "pair": pair,
                "maxTradeSize": max_trade_size,
                "riskLevel": risk_level,
                "updatedAt": now_utc(),
            },
            "$setOnInsert": {"createdAt": now_utc()},
        },
        upsert=True,
    )
    print(f"[Audi Bot] Saved settings for {pair}")


def clear_settings(pair, max_trade_size=None, risk_level=None):
    ensure_table()
    mongo_db().audi_bot_settings.update_one(
        {"pair": pair},
        {
            "$set": {
                "maxTradeSize": None,
                "riskLevel": None,
                "updatedAt": now_utc(),
            }
        },
        upsert=False,
    )
    print(f"[Audi Bot] Cleared settings for {pair}")


def _project(row):
    if not row:
        return {}
    return {
        "pair": row.get("pair"),
        "maxTradeSize": row.get("maxTradeSize"),
        "riskLevel": row.get("riskLevel"),
    }


def get_settings(pair=None):
    ensure_table()
    if pair:
        return get_settings_for_pair(pair)
    return [_project(row) for row in mongo_db().audi_bot_settings.find({}, {"_id": False})]


def get_settings_for_pair(pair):
    ensure_table()
    row = mongo_db().audi_bot_settings.find_one({"pair": pair}, {"_id": False})
    return _project(row)


def get_bot_settings():
    settings = mongo_db().app_settings.find_one({"key": "audi_bot_strategy"}, {"_id": False})
    value = (settings or {}).get("value", {})
    merged = {**DEFAULT_BOT_SETTINGS, **value}
    merged["strategyEnabled"] = bool(merged.get("strategyEnabled", False))
    merged["strategyIntervalMinutes"] = int(merged.get("strategyIntervalMinutes", 5))
    merged["ollamaUrl"] = str(merged.get("ollamaUrl", "http://127.0.0.1:11434"))
    merged["maxPaperTradeSize"] = float(merged.get("maxPaperTradeSize", 100.0))
    merged["minDecisionIntervalMinutes"] = int(merged.get("minDecisionIntervalMinutes", 5))
    merged["maxDecisionsPerHour"] = int(merged.get("maxDecisionsPerHour", 12))
    return merged


def save_bot_settings(data):
    payload = {**DEFAULT_BOT_SETTINGS, **(data or {})}
    payload["strategyEnabled"] = bool(payload.get("strategyEnabled", False))
    payload["strategyIntervalMinutes"] = int(payload.get("strategyIntervalMinutes", 5))
    payload["ollamaUrl"] = str(payload.get("ollamaUrl", "http://127.0.0.1:11434"))
    payload["maxPaperTradeSize"] = float(payload.get("maxPaperTradeSize", 100.0))
    payload["minDecisionIntervalMinutes"] = int(payload.get("minDecisionIntervalMinutes", 5))
    payload["maxDecisionsPerHour"] = int(payload.get("maxDecisionsPerHour", 12))
    mongo_db().app_settings.update_one(
        {"key": "audi_bot_strategy"},
        {"$set": {"key": "audi_bot_strategy", "value": payload, "updatedAt": now_utc()}},
        upsert=True,
    )
    return payload
