"""Fail-closed operator authentication and append-only mutation audit."""

from functools import wraps
from secrets import compare_digest
from typing import Any, Callable

from flask import current_app, jsonify, request

from .db import database_service, now_utc


def append_audit(event_type: str, outcome: str, metadata: dict[str, Any] | None = None) -> None:
    database_service().collection("audit_events").insert_one({
        "schema_version": 1,
        "event_type": event_type,
        "outcome": outcome,
        "actor": "operator",
        "timestamp": now_utc(),
        "metadata": metadata or {},
    })


def operator_required(event_type: str) -> Callable:
    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapped(*args: Any, **kwargs: Any):
            settings = current_app.config["AUTOLUNO_SETTINGS"]
            supplied = request.headers.get("X-AutoLuno-Token", "")
            if not settings.operator_token or not supplied or not compare_digest(
                settings.operator_token, supplied
            ):
                return jsonify({"error": "operator authentication required"}), 403
            result = function(*args, **kwargs)
            append_audit(event_type, "accepted", {"path": request.path, "method": request.method})
            return result
        return wrapped
    return decorator
