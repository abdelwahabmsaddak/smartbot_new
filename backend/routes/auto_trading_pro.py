from flask import Blueprint, request, jsonify
from backend.services.ai_signals_service import generate_signal
from backend.services.trading_engine import run_auto_trade

auto_trading_pro_bp = Blueprint("auto_trading_pro", __name__, url_prefix="/api/auto-trading-pro")

@auto_trading_pro_bp.route("/run", methods=["POST"])
def run():
    """
    Body مثال:
    {
      "asset": "BTC/USDT",
      "timeframe": "1h",
      "market": "crypto",
      "halal_strict": true,
      "account": {
        "symbol": "BTC/USDT",
        "balance": 1000,
        "risk": 1,
        "mode": "paper",
        "exchange": "binance",
        "type": "MARKET"
      }
    }
    """
    try:
        data = request.get_json() or {}

        asset = data.get("asset")
        timeframe = data.get("timeframe", "1h")
        market = data.get("market", "crypto")
        halal_strict = bool(data.get("halal_strict", True))

        account = data.get("account") or {}
        # لو ما بعثش symbol نستعمل asset
        account.setdefault("symbol", asset)
        account.setdefault("timeframe", timeframe)
        account.setdefault("mode", "paper")

        if not asset:
            return jsonify({"error": "asset is required"}), 400

        # 1) AI يولّد Signal
        signal = generate_signal(asset, timeframe, market, halal_strict=halal_strict)

        # حماية بسيطة: إذا الثقة ضعيفة، ما ننفّذوش
        min_conf = int(data.get("min_confidence", 60))
        if signal.get("confidence", 0) < min_conf:
            return jsonify({
                "status": "SKIPPED",
                "reason": f"Low confidence < {min_conf}",
                "signal": signal
            })

        # 2) Engine ينفّذ (Paper افتراضي)
        result = run_auto_trade(signal, account)

        return jsonify({
            "status": "OK",
            "signal": signal,
            "execution": result
        })

    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
