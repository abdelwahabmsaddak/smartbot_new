from flask import Blueprint, request, jsonify
from backend.services.ai_signals_service import generate_signal
from backend.services.risk_manager import validate_signal
from backend.execution.engine import run_auto_trade

auto_trading_pro_bp = Blueprint(
    "auto_trading_pro",
    __name__,
    url_prefix="/api/auto-trading-pro"
)

@auto_trading_pro_bp.route("/run", methods=["POST"])
def run():
    try:
        data = request.get_json()

        asset = data.get("asset")
        timeframe = data.get("timeframe", "1h")
        market = data.get("market", "crypto")
        min_conf = int(data.get("min_confidence", 60))

        account = data.get("account", {})
        user_id = data.get("user_id", "demo")

        if not asset:
            return jsonify({"status": "ERROR", "msg": "Asset required"}), 400

        # 1️⃣ AI Signal
        signal = generate_signal(asset, timeframe, market)

        # 2️⃣ Risk Filter
        ok, reason = validate_signal(signal, min_conf)
        if not ok:
            return jsonify({
                "status": "SKIPPED",
                "reason": reason,
                "signal": signal
            })

        # 3️⃣ Execute
        result = run_auto_trade(signal, account, user_id)

        return jsonify({
            "status": "EXECUTED",
            "signal": signal,
            "execution": result
        })

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500
