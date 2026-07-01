from database.mongo import mongo_db, now_utc


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
