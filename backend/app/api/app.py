from flask import Blueprint, current_app, jsonify, request

from backend.app.core import (
    grouped_history,
    list_collection,
    get_feesinfo_settings,
    upsert_feesinfo_settings,
    get_marketsinfo_settings,
    upsert_marketsinfo_settings,
    get_tradesinfo_settings,
    upsert_tradesinfo_settings,
    get_luno_status,
)
from backend.app.core.safety import operator_required

app_bp = Blueprint("app_bp", __name__)


@app_bp.get("/api/health")
def health_api():
    return jsonify({"status": "ok", "service": "autoluno-backend"})


@app_bp.get("/api/ready")
def ready_api():
    from backend.app.core.db import database_service
    from backend.app.services.ai_providers import create_ai_provider
    mongodb = database_service().status()
    settings = current_app.config["AUTOLUNO_SETTINGS"]
    ai_state = "disabled"
    if settings.ai_enabled:
        ai_state = create_ai_provider(settings.ai_provider, url=settings.ollama_url).status()["state"]
    body = {"status": "ready" if mongodb["ok"] else "not_ready",
            "required_services": {"mongodb": mongodb["state"]},
            "optional_services": {"qdrant": "disabled", "searxng": "disabled", "ai": ai_state}}
    return jsonify(body), 200 if mongodb["ok"] else 503


@app_bp.get("/api/server-time")
def server_time_api():
    from datetime import datetime, timezone
    return jsonify({"serverTime": datetime.now(timezone.utc).isoformat()})


@app_bp.get("/api/1/ticker/history")
def ticker_history_api():
    return jsonify(grouped_history("ticker_history", "pair"))


@app_bp.get("/api/1/balance/history")
def balance_history_api():
    return jsonify(grouped_history("balance_history", "asset"))


@app_bp.get("/api/1/trade/history")
def trade_history_api():
    return jsonify(grouped_history("trade_history", "pair"))


@app_bp.get("/api/1/fee/history")
def fee_history_api():
    return jsonify(grouped_history("fee_history", "pair"))


@app_bp.get("/api/1/marketsInfo/history")
def markets_history_api():
    return jsonify(grouped_history("market_history", "pair"))


@app_bp.get("/api/1/pairs")
def pairs_list_api():
    return jsonify(list_collection("pairs_list"))


@app_bp.get("/api/1/assets")
def assets_list_api():
    return jsonify(list_collection("assets_list"))


@app_bp.get("/api/app/settings/getfeeinfo")
def app_getfees_settings():
    return jsonify(get_feesinfo_settings())


@app_bp.post("/api/app/settings/savefeeinfo")
@operator_required("settings_fees_updated")
def app_savefee_settings():
    data = request.get_json()
    auto_fetch = data.get("autoFetch")
    auto_fetch_time = data.get("autoFetchTime")
    if auto_fetch is None or auto_fetch_time is None:
        return jsonify({"error": "Missing 'autoFetch' or 'autoFetchTime' field"}), 400
    upsert_feesinfo_settings(auto_fetch, auto_fetch_time)
    return jsonify({"message": "Settings saved successfully"})


@app_bp.get("/api/app/settings/getmarketinfo")
def app_getmarket_settings():
    return jsonify(get_marketsinfo_settings())


@app_bp.post("/api/app/settings/savemarketinfo")
@operator_required("settings_markets_updated")
def app_savemarket_settings():
    data = request.get_json()
    auto_fetch = data.get("autoFetch")
    auto_fetch_time = data.get("autoFetchTime")
    if auto_fetch is None or auto_fetch_time is None:
        return jsonify({"error": "Missing 'autoFetch' or 'autoFetchTime' field"}), 400
    upsert_marketsinfo_settings(auto_fetch, auto_fetch_time)
    return jsonify({"message": "Settings saved successfully"})


@app_bp.get("/api/app/settings/gettradeinfo")
def app_gettrade_settings():
    return jsonify(get_tradesinfo_settings())


@app_bp.post("/api/app/settings/savetradeinfo")
@operator_required("settings_trades_updated")
def app_savetrade_settings():
    data = request.get_json()
    auto_fetch = data.get("autoFetch")
    auto_fetch_time = data.get("autoFetchTime")
    if auto_fetch is None or auto_fetch_time is None:
        return jsonify({"error": "Missing 'autoFetch' or 'autoFetchTime' field"}), 400
    upsert_tradesinfo_settings(auto_fetch, auto_fetch_time)
    return jsonify({"message": "Settings saved successfully"})


@app_bp.get("/api/app/settings")
def app_get_all_settings():
    return jsonify(
        {
            "feesInfoSetting": get_feesinfo_settings(),
            "marketsInfoSetting": get_marketsinfo_settings(),
            "tradesSetting": get_tradesinfo_settings(),
        }
    )


@app_bp.get("/api/luno/status")
def luno_status_api():
    return jsonify(get_luno_status())
