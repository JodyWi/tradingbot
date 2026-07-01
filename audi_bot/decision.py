from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from database.mongo import mongo_db, now_utc
from backend.luno_functions.luno_live import (
    get_live_ticker,
    get_live_orderbook_top,
)
from audi_bot.utils import get_bot_settings


ALLOWED_ACTIONS = {"buy", "sell", "hold"}


@dataclass(frozen=True)
class DecisionOutcome:
    action: str
    confidence: float
    reason: str
    size: float
    raw_response: Any = None
    prompt: str | None = None
    execution_result: str = "not_executed"
    capped_size: float | None = None


def build_prompt(pair: str, ticker: dict[str, Any], orderbook: dict[str, Any], settings: dict[str, Any]) -> str:
    payload = {
        "pair": pair,
        "ticker": {
            "bid": ticker.get("bid"),
            "ask": ticker.get("ask"),
            "last_trade": ticker.get("last_trade"),
            "status": ticker.get("status"),
        },
        "orderbook_top": {
            "bids": orderbook.get("bids", [])[:1],
            "asks": orderbook.get("asks", [])[:1],
        },
        "policy": {
            "max_paper_trade_size": settings["maxPaperTradeSize"],
            "allowed_actions": sorted(ALLOWED_ACTIONS),
            "decision_schema": {
                "action": "buy|sell|hold",
                "confidence": "0..1",
                "reason": "short explanation",
                "size": "positive number",
            },
        },
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def parse_model_response(raw: str) -> dict[str, Any]:
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("response must be a JSON object")

    action = str(data.get("action", "")).strip().lower()
    if action not in ALLOWED_ACTIONS:
        raise ValueError("invalid action")

    if "confidence" not in data or data.get("confidence") in (None, ""):
        raise ValueError("missing confidence")
    confidence = float(data.get("confidence"))
    if confidence < 0 or confidence > 1:
        raise ValueError("invalid confidence")

    reason = str(data.get("reason", "")).strip()
    if not reason:
        raise ValueError("missing reason")

    if "size" not in data or data.get("size") in (None, ""):
        raise ValueError("missing size")
    size = float(data.get("size"))
    if size < 0:
        raise ValueError("invalid size")

    return {
        "action": action,
        "confidence": confidence,
        "reason": reason,
        "size": size,
    }


def call_ollama(prompt: str, *, model: str) -> str:
    base_url = (get_bot_settings().get("ollamaUrl") or "").strip() or "http://127.0.0.1:11434"
    response = requests.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "stream": False,
            "messages": [
                {"role": "system", "content": "Return only strict JSON with keys action, confidence, reason, size."},
                {"role": "user", "content": prompt},
            ],
            "format": "json",
        },
        timeout=10,
    )
    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.status_code} {response.text}")
    payload = response.json()
    content = payload.get("message", {}).get("content", "")
    if not content:
        raise ValueError("empty ollama response")
    return content


def _paper_trade_allowed(now: datetime, settings: dict[str, Any]) -> tuple[bool, str]:
    if not settings.get("strategyEnabled", False):
        return False, "strategy disabled"
    return True, ""


def _hard_cap_size(size: float, settings: dict[str, Any]) -> float:
    return min(size, float(settings["maxPaperTradeSize"]))


def _recent_decision_count(pair: str, since: datetime) -> int:
    return mongo_db().bot_decision_log.count_documents({
        "pair": pair,
        "createdAt": {"$gte": since},
    })


def _last_decision_time(pair: str) -> datetime | None:
    row = mongo_db().bot_decision_log.find_one(
        {"pair": pair},
        sort=[("createdAt", -1)],
        projection={"createdAt": 1},
    )
    return row.get("createdAt") if row else None


def _log_decision(document: dict[str, Any]) -> None:
    mongo_db().bot_decision_log.insert_one(dict(document))


def _serialize_document(document: dict[str, Any]) -> dict[str, Any]:
    result = dict(document)
    if "_id" in result:
        result["_id"] = str(result["_id"])
    if "createdAt" in result and hasattr(result["createdAt"], "isoformat"):
        result["createdAt"] = result["createdAt"].isoformat()
    return result


def run_decision_cycle(pair: str, paper_executor=None) -> dict[str, Any]:
    settings = get_bot_settings()
    now = now_utc()
    enabled, reason = _paper_trade_allowed(now, settings)
    if not enabled:
        document = {
            "pair": pair,
            "createdAt": now,
            "prompt": None,
            "rawResponse": None,
            "parsedAction": "hold",
            "executionResult": f"hold due to {reason}",
            "reason": reason,
        }
        _log_decision(document)
        return _serialize_document(document)

    min_interval = timedelta(minutes=int(settings["minDecisionIntervalMinutes"]))
    last_time = _last_decision_time(pair)
    if last_time and now - last_time < min_interval:
        document = {
            "pair": pair,
            "createdAt": now,
            "prompt": None,
            "rawResponse": None,
            "parsedAction": "hold",
            "executionResult": "hold due to minimum interval cap",
            "reason": "minimum interval cap",
        }
        _log_decision(document)
        return _serialize_document(document)

    hourly_limit = int(settings["maxDecisionsPerHour"])
    if _recent_decision_count(pair, now - timedelta(hours=1)) >= hourly_limit:
        document = {
            "pair": pair,
            "createdAt": now,
            "prompt": None,
            "rawResponse": None,
            "parsedAction": "hold",
            "executionResult": "hold due to hourly cap",
            "reason": "hourly cap",
        }
        _log_decision(document)
        return _serialize_document(document)

    ticker = get_live_ticker(pair)
    orderbook = get_live_orderbook_top(pair)
    prompt = build_prompt(pair, ticker, orderbook, settings)

    raw_response = None
    try:
        raw_response = call_ollama(prompt, model=settings["model"])
        parsed = parse_model_response(raw_response)
        capped_size = _hard_cap_size(float(parsed["size"]), settings)
        decision = dict(parsed)
        decision["size"] = capped_size
        if parsed["action"] == "hold":
            execution_result = "hold"
        elif paper_executor is None:
            execution_result = "paper executor unavailable"
        else:
            execution_result = paper_executor(pair=pair, action=parsed["action"], size=capped_size, ticker=ticker, orderbook=orderbook)
        document = {
            "pair": pair,
            "createdAt": now,
            "prompt": prompt,
            "rawResponse": raw_response,
            "parsedAction": decision,
            "executionResult": execution_result,
            "reason": decision["reason"],
        }
        _log_decision(document)
        return _serialize_document(document)
    except (ValueError, json.JSONDecodeError) as exc:
        document = {
            "pair": pair,
            "createdAt": now,
            "prompt": prompt,
            "rawResponse": raw_response,
            "parsedAction": "hold",
            "executionResult": "hold due to malformed model output",
            "reason": "malformed model output",
        }
        _log_decision(document)
        return _serialize_document(document)
    except Exception as exc:
        document = {
            "pair": pair,
            "createdAt": now,
            "prompt": prompt,
            "rawResponse": str(exc),
            "parsedAction": "hold",
            "executionResult": "hold due to Ollama error",
            "reason": "ollama error",
        }
        _log_decision(document)
        return _serialize_document(document)
