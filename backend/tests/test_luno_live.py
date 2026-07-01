import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.main import app
from backend.luno_functions import luno_live


class DummyResponse:
    def __init__(self, status_code=200, payload=None, text="ok"):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


def test_live_ticker_requires_pair():
    with pytest.raises(ValueError):
        luno_live.get_live_ticker("")


def test_live_ticker_returns_timestamp(monkeypatch):
    monkeypatch.setattr(luno_live.requests, "get", lambda *a, **k: DummyResponse(payload={
        "pair": "XBTZAR",
        "timestamp": 1000,
        "bid": "1",
        "ask": "2",
        "last_trade": "3",
        "rolling_24_hour_volume": "4",
        "status": "ACTIVE",
    }))

    result = luno_live.get_live_ticker("XBTZAR")
    assert result["pair"] == "XBTZAR"
    assert "timestamp" in result


def test_live_orderbook_top_returns_payload(monkeypatch):
    captured = {}

    monkeypatch.setattr(luno_live.requests, "get", lambda *a, **k: DummyResponse(payload={
        "pair": "XBTZAR",
        "bids": [{"price": "1", "volume": "2"}],
        "asks": [{"price": "3", "volume": "4"}],
    }))

    result = luno_live.get_live_orderbook_top("XBTZAR")
    assert result["pair"] == "XBTZAR"
    assert result["bids"][0]["price"] == "1"


def test_live_trades_requires_pair():
    with pytest.raises(ValueError):
        luno_live.get_live_trades("")


def test_live_trades_uses_auth(monkeypatch):
    seen = {}

    def fake_get(url, **kwargs):
        seen["url"] = url
        seen["auth"] = kwargs.get("auth")
        return DummyResponse(payload={
            "trades": [{"pair": "XBTZAR", "sequence": 1}],
        })

    monkeypatch.setattr(luno_live.requests, "get", fake_get)
    result = luno_live.get_live_trades("XBTZAR")
    assert result["trades"][0]["pair"] == "XBTZAR"
    assert seen["url"].endswith("/api/1/listtrades")
    assert seen["auth"] is not None


def test_live_markets_returns_payload(monkeypatch):
    monkeypatch.setattr(luno_live.requests, "get", lambda *a, **k: DummyResponse(payload={
        "markets": [{"market_id": "XBTZAR"}],
    }))

    result = luno_live.get_live_markets("XBTZAR")
    assert result["markets"][0]["market_id"] == "XBTZAR"


def test_live_routes_expose_read_only_data(monkeypatch):
    monkeypatch.setattr("backend.app.api.luno.get_live_ticker", lambda pair: {"pair": pair, "source": "ticker"})
    monkeypatch.setattr("backend.app.api.luno.get_live_tickers", lambda: {"tickers": []})
    monkeypatch.setattr("backend.app.api.luno.get_live_orderbook_top", lambda pair: {"pair": pair, "source": "orderbook"})
    monkeypatch.setattr("backend.app.api.luno.get_live_trades", lambda pair: {"pair": pair, "source": "trades"})
    monkeypatch.setattr("backend.app.api.luno.get_live_markets", lambda pair=None: {"pair": pair, "source": "markets"})

    client = app.test_client()

    assert client.get("/api/luno/live/ticker?pair=XBTZAR").get_json()["source"] == "ticker"
    assert client.get("/api/luno/live/tickers").get_json()["tickers"] == []
    assert client.get("/api/luno/live/orderbook-top?pair=XBTZAR").get_json()["source"] == "orderbook"
    assert client.get("/api/luno/live/trades?pair=XBTZAR").get_json()["source"] == "trades"
    assert client.get("/api/luno/live/markets?pair=XBTZAR").get_json()["source"] == "markets"
