from flask import Blueprint, jsonify, request
from backend.execution.trade_store import get_user_trades

history_bp = Blueprint(
    "trade_history",
    __name__,
    url_prefix="/api/history"
)

@history_bp.route("/", methods=["GET"])
def trade_history():
    user_id = request.args.get("user", "demo")
    trades = get_user_trades(user_id)

    return jsonify({
        "status": "OK",
        "count": len(trades),
        "trades": trades
    })
