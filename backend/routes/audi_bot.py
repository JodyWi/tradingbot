from flask import Blueprint, jsonify, request

from audi_bot.utils import save_settings, get_settings, clear_settings, get_settings_for_pair
from audi_bot.runner import start as start_audi_bot

audi_bot_routes = Blueprint("audi_bot_routes", __name__)


@audi_bot_routes.get("/api/audi_bot/settings")
def audi_bot_get_settings():
    return jsonify(get_settings())


@audi_bot_routes.get("/api/audi_bot/settings/<pair>")
def audi_bot_get_settings_for_pair(pair):
    return jsonify(get_settings_for_pair(pair))


@audi_bot_routes.post("/api/audi_bot/settings/save")
def audi_bot_save_settings():
    data = request.get_json()
    pair = data.get("pair")
    max_trade_size = data.get("maxTradeSize")
    risk_level = data.get("riskLevel")
    if not pair:
        return jsonify({"error": "Missing 'pair' field"}), 400
    save_settings(pair, max_trade_size, risk_level)
    return jsonify({"message": f"Settings saved for pair: {pair}"})


@audi_bot_routes.delete("/api/audi_bot/settings/clear")
def audi_bot_clear_settings():
    data = request.get_json()
    pair = data.get("pair")
    max_trade_size = data.get("maxTradeSize")
    risk_level = data.get("riskLevel")
    if not pair:
        return jsonify({"error": "Missing 'pair' field"}), 400
    clear_settings(pair, max_trade_size, risk_level)
    return jsonify({"message": f"Settings cleared for pair: {pair}"})


@audi_bot_routes.post("/api/audi_bot/start")
def audi_bot_start():
    start_audi_bot()
    return jsonify({"status": "paper_only", "message": "Audi Bot lifecycle acknowledged. Live Luno order execution is not enabled."})


@audi_bot_routes.post("/api/audi_bot/stop")
def audi_bot_stop():
    return jsonify({"status": "stopped", "message": "Audi Bot stopped. No live Luno order execution was enabled."})
