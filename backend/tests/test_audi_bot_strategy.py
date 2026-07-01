import json
import os
import sys
from datetime import datetime, timezone, timedelta
from bson import BSON

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from audi_bot import decision as bot_decision
from audi_bot import runner as bot_runner
from backend.app.main import app


class DummyResponse:
    def __init__(self, status_code=200, payload=None, text="ok"):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


class DummyCollection:
    def __init__(self):
        self.docs = []
        self.last_query = None

    def insert_one(self, doc):
        self.docs.append(doc)

    def count_documents(self, query):
        self.last_query = query
        return 0

    def find_one(self, *args, **kwargs):
        sort = kwargs.get("sort")
        if self.docs and sort:
            return self.docs[-1]
        return self.docs[-1] if self.docs else None


class DummyDB:
    def __init__(self):
        self.bot_decision_log = DummyCollection()
        self.app_settings = DummyCollection()


def test_parse_model_response_accepts_strict_json():
    parsed = bot_decision.parse_model_response(
        json.dumps({"action": "buy", "confidence": 0.7, "reason": "trend", "size": 12})
    )
    assert parsed["action"] == "buy"
    assert parsed["confidence"] == 0.7
    assert parsed["size"] == 12


@pytest.mark.parametrize(
    "payload",
    [
        "{}",
        json.dumps({"action": "jump", "confidence": 0.7, "reason": "x", "size": 1}),
        json.dumps({"action": "buy", "confidence": 2, "reason": "x", "size": 1}),
        json.dumps({"action": "buy", "confidence": 0.7, "reason": "", "size": 1}),
        json.dumps({"action": "buy", "confidence": 0.7, "reason": "x", "size": -1}),
    ],
)
def test_parse_model_response_rejects_bad_json(payload):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        bot_decision.parse_model_response(payload)


def test_run_decision_cycle_fails_closed_on_malformed_model_output(monkeypatch):
    db = DummyDB()

    monkeypatch.setattr(bot_decision, "get_bot_settings", lambda: {
        "strategyEnabled": True,
        "strategyIntervalMinutes": 5,
        "model": "qwen2.5-coder:0.5b",
        "ollamaUrl": "http://127.0.0.1:11434",
        "maxPaperTradeSize": 100.0,
        "minDecisionIntervalMinutes": 5,
        "maxDecisionsPerHour": 12,
    })
    monkeypatch.setattr(bot_decision, "get_live_ticker", lambda pair: {"pair": pair, "bid": "1", "ask": "2", "last_trade": "1.5", "status": "ACTIVE"})
    monkeypatch.setattr(bot_decision, "get_live_orderbook_top", lambda pair: {"bids": [{"price": "1"}], "asks": [{"price": "2"}]})
    monkeypatch.setattr(bot_decision, "call_ollama", lambda *a, **k: "not-json")
    monkeypatch.setattr(bot_decision, "mongo_db", lambda: db)

    result = bot_decision.run_decision_cycle("XBTZAR")
    assert result["parsedAction"] == "hold"
    assert result["executionResult"] == "hold due to malformed model output"
    assert db.bot_decision_log.docs[0]["rawResponse"] == "not-json"


def test_run_decision_cycle_fails_closed_when_ollama_unreachable(monkeypatch):
    db = DummyDB()

    monkeypatch.setattr(bot_decision, "get_bot_settings", lambda: {
        "strategyEnabled": True,
        "strategyIntervalMinutes": 5,
        "model": "qwen2.5-coder:0.5b",
        "ollamaUrl": "http://127.0.0.1:11434",
        "maxPaperTradeSize": 100.0,
        "minDecisionIntervalMinutes": 5,
        "maxDecisionsPerHour": 12,
    })
    monkeypatch.setattr(bot_decision, "get_live_ticker", lambda pair: {"pair": pair, "bid": "1", "ask": "2", "last_trade": "1.5", "status": "ACTIVE"})
    monkeypatch.setattr(bot_decision, "get_live_orderbook_top", lambda pair: {"bids": [{"price": "1"}], "asks": [{"price": "2"}]})
    monkeypatch.setattr(bot_decision, "call_ollama", lambda *a, **k: (_ for _ in ()).throw(Exception("down")))
    monkeypatch.setattr(bot_decision, "mongo_db", lambda: db)

    result = bot_decision.run_decision_cycle("XBTZAR")
    assert result["parsedAction"] == "hold"
    assert result["executionResult"] == "hold due to Ollama error"


def test_hard_cap_enforced(monkeypatch):
    executed = {}
    db = DummyDB()

    monkeypatch.setattr(bot_decision, "get_bot_settings", lambda: {
        "strategyEnabled": True,
        "strategyIntervalMinutes": 5,
        "model": "qwen2.5-coder:0.5b",
        "ollamaUrl": "http://127.0.0.1:11434",
        "maxPaperTradeSize": 2.5,
        "minDecisionIntervalMinutes": 5,
        "maxDecisionsPerHour": 12,
    })
    monkeypatch.setattr(bot_decision, "get_live_ticker", lambda pair: {"pair": pair, "bid": "1", "ask": "2", "last_trade": "1.5", "status": "ACTIVE"})
    monkeypatch.setattr(bot_decision, "get_live_orderbook_top", lambda pair: {"bids": [{"price": "1"}], "asks": [{"price": "2"}]})
    monkeypatch.setattr(bot_decision, "call_ollama", lambda *a, **k: json.dumps({"action": "buy", "confidence": 0.9, "reason": "x", "size": 50}))
    monkeypatch.setattr(bot_decision, "mongo_db", lambda: db)

    result = bot_decision.run_decision_cycle("XBTZAR", paper_executor=lambda **kwargs: executed.setdefault("kwargs", kwargs) or "paper ok")
    assert result["parsedAction"]["size"] == 2.5
    assert executed["kwargs"]["size"] == 2.5


def test_start_disabled_by_default(monkeypatch):
    monkeypatch.setattr(bot_runner, "get_bot_settings", lambda: {"strategyEnabled": False})
    result = bot_runner.start("XBTZAR")
    assert result["status"] == "disabled"


def test_run_strategy_once_endpoint_serializes_response(monkeypatch):
    db = DummyDB()

    monkeypatch.setattr(bot_decision, "mongo_db", lambda: db)
    monkeypatch.setattr(bot_decision, "get_bot_settings", lambda: {
        "strategyEnabled": True,
        "strategyIntervalMinutes": 5,
        "model": "qwen2.5-coder:0.5b",
        "ollamaUrl": "http://127.0.0.1:11434",
        "maxPaperTradeSize": 2.5,
        "minDecisionIntervalMinutes": 5,
        "maxDecisionsPerHour": 12,
    })
    monkeypatch.setattr(bot_decision, "get_live_ticker", lambda pair: {"pair": pair, "bid": "1", "ask": "2", "last_trade": "1.5", "status": "ACTIVE"})
    monkeypatch.setattr(bot_decision, "get_live_orderbook_top", lambda pair: {"bids": [{"price": "1"}], "asks": [{"price": "2"}]})
    monkeypatch.setattr(bot_decision, "call_ollama", lambda *a, **k: json.dumps({"action": "hold", "confidence": 0.6, "reason": "wait", "size": 1}))

    client = app.test_client()
    response = client.post("/api/audi_bot/strategy/run", json={"pair": "XBTZAR"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["parsedAction"]["action"] == "hold"
    assert isinstance(payload["createdAt"], str)
    assert "_id" not in payload or isinstance(payload["_id"], str)


def test_min_interval_cap_handles_bson_round_trip_datetime(monkeypatch):
    db = DummyDB()
    past = datetime.now(timezone.utc)
    stored = {
        "pair": "XBTZAR",
        "createdAt": BSON(BSON.encode({"createdAt": past})).decode()["createdAt"],
    }
    db.bot_decision_log.docs.append(stored)

    monkeypatch.setattr(bot_decision, "mongo_db", lambda: db)
    monkeypatch.setattr(bot_decision, "get_bot_settings", lambda: {
        "strategyEnabled": True,
        "strategyIntervalMinutes": 5,
        "model": "qwen2.5-coder:0.5b",
        "ollamaUrl": "http://127.0.0.1:11434",
        "maxPaperTradeSize": 2.5,
        "minDecisionIntervalMinutes": 5,
        "maxDecisionsPerHour": 12,
    })
    monkeypatch.setattr(bot_decision, "get_live_ticker", lambda pair: {"pair": pair, "bid": "1", "ask": "2", "last_trade": "1.5", "status": "ACTIVE"})
    monkeypatch.setattr(bot_decision, "get_live_orderbook_top", lambda pair: {"bids": [{"price": "1"}], "asks": [{"price": "2"}]})
    monkeypatch.setattr(bot_decision, "call_ollama", lambda *a, **k: json.dumps({"action": "buy", "confidence": 0.9, "reason": "x", "size": 1}))

    result = bot_decision.run_decision_cycle("XBTZAR")
    assert result["executionResult"] == "capped, skipped: minimum interval"


def test_run_strategy_once_endpoint_can_be_called_repeatedly_without_crashing(monkeypatch):
    db = DummyDB()
    past = datetime.now(timezone.utc) - timedelta(minutes=10)
    db.bot_decision_log.docs.append({"pair": "XBTZAR", "createdAt": BSON(BSON.encode({"createdAt": past})).decode()["createdAt"]})

    monkeypatch.setattr(bot_decision, "mongo_db", lambda: db)
    monkeypatch.setattr(bot_decision, "get_bot_settings", lambda: {
        "strategyEnabled": True,
        "strategyIntervalMinutes": 5,
        "model": "qwen2.5-coder:0.5b",
        "ollamaUrl": "http://127.0.0.1:11434",
        "maxPaperTradeSize": 2.5,
        "minDecisionIntervalMinutes": 5,
        "maxDecisionsPerHour": 12,
    })
    monkeypatch.setattr(bot_decision, "get_live_ticker", lambda pair: {"pair": pair, "bid": "1", "ask": "2", "last_trade": "1.5", "status": "ACTIVE"})
    monkeypatch.setattr(bot_decision, "get_live_orderbook_top", lambda pair: {"bids": [{"price": "1"}], "asks": [{"price": "2"}]})
    monkeypatch.setattr(bot_decision, "call_ollama", lambda *a, **k: json.dumps({"action": "buy", "confidence": 0.9, "reason": "x", "size": 1}))

    first = bot_decision.run_decision_cycle("XBTZAR")
    second = bot_decision.run_decision_cycle("XBTZAR")
    third = bot_decision.run_decision_cycle("XBTZAR")

    assert first["executionResult"] in {"hold", "paper executor unavailable"}
    assert second["executionResult"] == "capped, skipped: minimum interval"
    assert third["executionResult"] == "capped, skipped: minimum interval"
