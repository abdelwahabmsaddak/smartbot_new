from flask import Blueprint, request, jsonify
from backend.services.trading_engine import run_auto_trade

auto_trading_bp = Blueprint(
    "auto_trading",
    __name__,
    url_prefix="/api/auto-trading"
)

@auto_trading_bp.route("/execute", methods=["POST"])
def execute_trade():
    try:
        data = request.get_json()

        signal = data.get("signal")
        account = data.get("account")

        if not signal or not account:
            return jsonify({"error": "Missing data"}), 400

        result = run_auto_trade(signal, account)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
