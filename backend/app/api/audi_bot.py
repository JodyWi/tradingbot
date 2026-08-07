from flask import Blueprint, jsonify, request

from autoluno.backend.audi_bot.utils import save_settings, get_settings, clear_settings, get_settings_for_pair, get_bot_settings, save_bot_settings
from autoluno.backend.audi_bot.runner import start as start_audi_bot, stop as stop_audi_bot, step as step_audi_bot
from backend.app.core.safety import operator_required

audi_bot_bp = Blueprint("audi_bot_bp", __name__)


@audi_bot_bp.get("/api/audi_bot/settings")
def audi_bot_get_settings():
    return jsonify(get_settings())


@audi_bot_bp.get("/api/audi_bot/settings/<pair>")
def audi_bot_get_settings_for_pair(pair):
    return jsonify(get_settings_for_pair(pair))


@audi_bot_bp.post("/api/audi_bot/settings/save")
@operator_required("audi_bot_settings_saved")
def audi_bot_save_settings():
    data = request.get_json()
    pair = data.get("pair")
    max_trade_size = data.get("maxTradeSize")
    risk_level = data.get("riskLevel")
    if not pair:
        return jsonify({"error": "Missing 'pair' field"}), 400
    save_settings(pair, max_trade_size, risk_level)
    return jsonify({"message": f"Settings saved for pair: {pair}"})


@audi_bot_bp.delete("/api/audi_bot/settings/clear")
@operator_required("audi_bot_settings_cleared")
def audi_bot_clear_settings():
    data = request.get_json()
    pair = data.get("pair")
    max_trade_size = data.get("maxTradeSize")
    risk_level = data.get("riskLevel")
    if not pair:
        return jsonify({"error": "Missing 'pair' field"}), 400
    clear_settings(pair, max_trade_size, risk_level)
    return jsonify({"message": f"Settings cleared for pair: {pair}"})


@audi_bot_bp.post("/api/audi_bot/start")
@operator_required("audi_bot_started")
def audi_bot_start():
    result = start_audi_bot()
    return jsonify(result)


@audi_bot_bp.post("/api/audi_bot/stop")
@operator_required("audi_bot_stopped")
def audi_bot_stop():
    result = stop_audi_bot()
    return jsonify(result)


@audi_bot_bp.get("/api/audi_bot/strategy")
def audi_bot_get_strategy_settings():
    return jsonify(get_bot_settings())


@audi_bot_bp.post("/api/audi_bot/strategy")
@operator_required("audi_bot_strategy_updated")
def audi_bot_save_strategy_settings():
    data = request.get_json() or {}
    result = save_bot_settings(data)
    return jsonify(result)


@audi_bot_bp.post("/api/audi_bot/strategy/run")
@operator_required("audi_bot_strategy_run")
def audi_bot_run_strategy_once():
    data = request.get_json() or {}
    pair = data.get("pair")
    if not pair:
        return jsonify({"error": "Missing 'pair' field"}), 400
    return jsonify(step_audi_bot(pair))
