from flask import Blueprint, jsonify
from backend.execution.engine import get_live_trades, get_stats

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)

@dashboard_bp.route("/live", methods=["GET"])
def live_dashboard():
    try:
        trades = get_live_trades()
        stats = get_stats(trades)

        return jsonify({
            "status": "OK",
            "stats": stats,
            "trades": trades
        })

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500
