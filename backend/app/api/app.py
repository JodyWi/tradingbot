from flask import Blueprint, jsonify, request

from backend.app.core import (
    grouped_history,
    list_collection,
    get_feesinfo_settings,
    upsert_feesinfo_settings,
    get_marketsinfo_settings,
    upsert_marketsinfo_settings,
    get_tradesinfo_settings,
    upsert_tradesinfo_settings,
)

app_bp = Blueprint("app_bp", __name__)


@app_bp.get("/api/health")
def health_api():
    return jsonify({"status": "ok", "storage": "mongo"})


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

