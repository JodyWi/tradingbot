import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.luno_functions import luno_ticker, luno_balance, luno_listTrades, luno_feeInfo, luno_marketsInfo


class DummyResponse:
    def __init__(self, status_code=200, payload=None, text="ok"):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


def test_ticker_requires_pair():
    with pytest.raises(ValueError):
        luno_ticker.get_ticker("")


def test_get_ticker_stores_and_returns_success(monkeypatch):
    captured = {}

    monkeypatch.setattr(luno_ticker.requests, "get", lambda *a, **k: DummyResponse(payload={
        "pair": "XBTZAR",
        "timestamp": 1000,
        "bid": "1",
        "ask": "2",
        "last_trade": "3",
        "rolling_24_hour_volume": "4",
        "status": "ACTIVE",
    }))
    monkeypatch.setattr(luno_ticker, "store_db", lambda rows: captured.setdefault("rows", rows))

    result = luno_ticker.get_ticker("XBTZAR")
    assert result["status"] == "success"
    assert result["pair"] == "XBTZAR"
    assert captured["rows"][0]["pair"] == "XBTZAR"


def test_get_balances_requires_assets(monkeypatch):
    with pytest.raises(ValueError):
        luno_balance.get_balance("")


def test_get_balances_success(monkeypatch):
    captured = {}
    monkeypatch.setattr(luno_balance.requests, "get", lambda *a, **k: DummyResponse(payload={
        "balance": [{"account_id": "1", "asset": "ZAR", "balance": "10", "reserved": "0", "unconfirmed": "0"}]
    }))
    monkeypatch.setattr(luno_balance, "store_db", lambda rows: captured.setdefault("rows", rows))

    result = luno_balance.get_balances()
    assert result["status"] == "success"
    assert result["count"] == 1
    assert captured["rows"][0]["asset"] == "ZAR"


def test_get_trade_requires_pair():
    with pytest.raises(ValueError):
        luno_listTrades.get_trade("")


def test_get_trade_success(monkeypatch):
    captured = {}
    monkeypatch.setattr(luno_listTrades.requests, "get", lambda *a, **k: DummyResponse(payload={
        "trades": [{"pair": "XBTZAR", "sequence": 1, "order_id": "abc", "type": "ASK", "timestamp": 1, "price": "1", "volume": "1", "base": "1", "counter": "1", "fee_base": "0", "fee_counter": "0", "is_buy": False, "client_order_id": ""}]
    }))
    monkeypatch.setattr(luno_listTrades, "store_db", lambda rows: captured.setdefault("rows", rows))

    result = luno_listTrades.get_trade("XBTZAR")
    assert result["status"] == "success"
    assert result["count"] == 1
    assert captured["rows"][0]["pair"] == "XBTZAR"


def test_fee_info_requires_pair():
    with pytest.raises(ValueError):
        luno_feeInfo.get_fee_info("")


def test_fee_info_success(monkeypatch):
    captured = {}
    monkeypatch.setattr(luno_feeInfo.requests, "get", lambda *a, **k: DummyResponse(payload={
        "maker_fee": "0.1",
        "taker_fee": "0.2",
        "thirty_day_volume": "1000",
    }))
    monkeypatch.setattr(luno_feeInfo, "store_db", lambda rows, pair: captured.setdefault("payload", (rows, pair)))

    result = luno_feeInfo.get_fee_info("XBTZAR")
    assert result["status"] == "success"
    assert captured["payload"][1] == "XBTZAR"


def test_markets_info_requires_pair():
    with pytest.raises(ValueError):
        luno_marketsInfo.get_markets_info("")


def test_markets_info_success(monkeypatch):
    captured = {}
    monkeypatch.setattr(luno_marketsInfo.requests, "get", lambda *a, **k: DummyResponse(payload={
        "markets": [{
            "base_currency": "XBT",
            "counter_currency": "ZAR",
            "fee_scale": 0,
            "market_id": "XBTZAR",
            "max_price": "1",
            "max_volume": "1",
            "min_price": "1",
            "min_volume": "1",
            "price_scale": 2,
            "trading_status": "ACTIVE",
            "volume_scale": 8,
        }]
    }))
    monkeypatch.setattr(luno_marketsInfo, "store_db", lambda rows, pair: captured.setdefault("payload", (rows, pair)))

    result = luno_marketsInfo.get_markets_info("XBTZAR")
    assert result["status"] == "success"
    assert captured["payload"][1] == "XBTZAR"
