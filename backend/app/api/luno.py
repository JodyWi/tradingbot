from flask import Blueprint, jsonify, request

from backend.luno_functions.luno_ticker import get_ticker, get_tickers
from backend.luno_functions.luno_balance import get_balance, get_balances
from backend.luno_functions.luno_listTrades import get_trade
from backend.luno_functions.luno_feeInfo import get_fee_info
from backend.luno_functions.luno_marketsInfo import get_markets_info

luno_bp = Blueprint("luno_bp", __name__)


@luno_bp.post("/api/1/ticker")
def get_ticker_api():
    pair = request.args.get("pair", default="")
    if not pair:
        return jsonify({"error": "pair is required"}), 400
    return jsonify(get_ticker(pair=pair))


@luno_bp.post("/api/1/tickers")
def get_tickers_api():
    return jsonify(get_tickers())


@luno_bp.post("/api/1/balance")
def get_balance_api():
    assets = request.args.get("assets", default="", type=str)
    return jsonify(get_balance(assets=assets))


@luno_bp.post("/api/1/balances")
def get_balances_api():
    return jsonify(get_balances())


@luno_bp.post("/api/1/trade")
def get_trade_api():
    pair = request.args.get("pair", default="LTCZAR")
    return jsonify(get_trade(pair=pair))


@luno_bp.post("/api/1/fee_info")
def get_fee_info_api():
    pair = request.args.get("pair", default="LTCZAR")
    return jsonify(get_fee_info(pair=pair))


@luno_bp.post("/api/1/markets_info")
def get_markets_info_api():
    pair = request.args.get("pair", default="LTCZAR")
    return jsonify(get_markets_info(pair=pair))

