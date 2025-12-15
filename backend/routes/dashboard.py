from flask import Blueprint, jsonify

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard_data():
    """
    API ترجع بيانات Dashboard
    (توّا mock – بعد نربطها بالـ AI و DB)
    """

    data = {
        "balance": 12450,
        "open_trades": 3,
        "ai_status": "active",
        "daily_profit": 320,
        "ai_logs": [
            "BUY BTC/USDT @ 43200",
            "SELL ETH/USDT @ 2450",
            "HOLD GOLD"
        ]
    }

    return jsonify(data)
