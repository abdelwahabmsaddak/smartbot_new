from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

ai_signals_bp = Blueprint("ai_signals_bp", __name__)

@ai_signals_bp.route("/signals", methods=["POST"])
def ai_signals():
    """
    إشارات تداول ذكية موحّدة:
    - Crypto
    - Gold
    - Halal Stocks
    """
    data = request.get_json() or {}

    asset = data.get("asset", "")              # مثال: BTC, ETH, GOLD, ARAMCO
    market = data.get("market", "auto")        # crypto / gold / stock / auto
    timeframe = data.get("timeframe", "4H")    # 15m / 1H / 4H / 1D
    risk_profile = data.get("risk", "medium")  # low / medium / high

    system_message = """
    You are SmartBot Unified AI — a professional trading signals engine.

    You generate actionable trading signals for:
    - Cryptocurrencies
    - Gold
    - Halal (Sharia-compliant) stocks

    Rules:
    - Identify the asset type automatically if not specified.
    - For stocks: ensure Sharia compliance.
    - Provide clear Buy/Sell/Hold signals.
    - Always include:
        Entry price
        Take-profit targets (TP1, TP2)
        Stop-loss
        Risk level
        Timeframe
    - Be conservative and realistic.
    """

    prompt = f"""
    Generate a trading signal with the following parameters:

    Asset: {asset or "Not specified"}
    Market: {market}
    Timeframe: {timeframe}
    Risk profile: {risk_profile}

    Please provide:
    1) Signal (Buy / Sell / Hold)
    2) Entry price or zone
    3) Take-profit targets (TP1, TP2)
    4) Stop-loss
    5) Risk level
    6) Probability of success (%)
    7) Short explanation
    """

    ai_reply = ai_chat(prompt, system_msg=system_message)

    return jsonify({
        "status": "success",
        "signal": ai_reply
    })
