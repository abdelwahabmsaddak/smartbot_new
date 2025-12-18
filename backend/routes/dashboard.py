from flask import Blueprint, jsonify

from backend.execution.trade_store import get_user_trades
from backend.execution.engine import get_stats

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/live", methods=["GET"])
def live_dashboard():
    user_id = "demo"

    trades = get_user_trades(user_id)
    stats = get_stats(trades)

    return jsonify({
        "status": "OK",
        "stats": stats,
        "trades": trades[-10:]
    })
