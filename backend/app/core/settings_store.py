from .db import get_setting, set_setting


DEFAULT_SETTING = {
    "autoFetch": False,
    "autoFetchTime": "23:00",
}


def _get_scheduler_setting(key):
    value = get_setting(key, DEFAULT_SETTING)
    return {
        "autoFetch": bool(value.get("autoFetch", False)),
        "autoFetchTime": value.get("autoFetchTime", "23:00"),
    }


def _upsert_scheduler_setting(key, autoFetch: bool, autoFetchTime: str):
    set_setting(
        key,
        {
            "autoFetch": bool(autoFetch),
            "autoFetchTime": autoFetchTime,
        },
    )


def get_feesinfo_settings():
    return _get_scheduler_setting("feesinfo")


def upsert_feesinfo_settings(autoFetch: bool, autoFetchTime: str):
    _upsert_scheduler_setting("feesinfo", autoFetch, autoFetchTime)


def get_marketsinfo_settings():
    return _get_scheduler_setting("marketsinfo")


def upsert_marketsinfo_settings(autoFetch: bool, autoFetchTime: str):
    _upsert_scheduler_setting("marketsinfo", autoFetch, autoFetchTime)


def get_tradesinfo_settings():
    return _get_scheduler_setting("tradesinfo")


def upsert_tradesinfo_settings(autoFetch: bool, autoFetchTime: str):
    _upsert_scheduler_setting("tradesinfo", autoFetch, autoFetchTime)

