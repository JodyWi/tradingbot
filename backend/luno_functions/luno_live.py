from __future__ import annotations

import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL", "").strip()
API_KEY = os.getenv("API_KEY", "").strip() or os.getenv("LUNO_API_KEY_ID", "").strip()
API_SECRET = os.getenv("API_SECRET", "").strip() or os.getenv("LUNO_API_KEY_SECRET", "").strip()

DEFAULT_TIMEOUT = 5


def _request(path: str, *, params: dict[str, str] | None = None, auth: bool = False) -> dict:
    if not LUNO_API_URL:
        raise ValueError("LUNO_API_URL is required")

    kwargs = {"params": params or {}, "timeout": DEFAULT_TIMEOUT}
    if auth:
        if not API_KEY or not API_SECRET:
            raise ValueError("Luno API credentials are required")
        kwargs["auth"] = (API_KEY, API_SECRET)

    response = requests.get(f"{LUNO_API_URL}{path}", **kwargs)
    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")
    return response.json()


def _stamp(payload: dict) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **payload,
    }


def get_live_ticker(pair: str) -> dict:
    if not pair:
        raise ValueError("pair is required")
    return _stamp(_request("/api/1/ticker", params={"pair": pair}))


def get_live_tickers() -> dict:
    return _stamp(_request("/api/1/tickers"))


def get_live_orderbook_top(pair: str) -> dict:
    if not pair:
        raise ValueError("pair is required")
    return _stamp(_request("/api/1/orderbook_top", params={"pair": pair}))


def get_live_trades(pair: str) -> dict:
    if not pair:
        raise ValueError("pair is required")
    return _stamp(_request("/api/1/listtrades", params={"pair": pair}, auth=True))


def get_live_markets(pair: str | None = None) -> dict:
    params = {"pair": pair} if pair else None
    return _stamp(_request("/api/exchange/1/markets", params=params))
