from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

whales_bp = Blueprint("whales_bp", __name__)

@whales_bp.route("/whales", methods=["POST"])
def whales_analysis():
    """
    تحليل الحيتان والسيولة:
    - Crypto
    - Gold
    - Halal Stocks
    """
    data = request.get_json() or {}

    asset = data.get("asset", "")                 # BTC, ETH, GOLD, ARAMCO
    market = data.get("market", "auto")           # crypto / gold / stock / auto
    timeframe = data.get("timeframe", "1D")       # 15m / 1H / 4H / 1D / 1W
    depth = data.get("depth", "medium")           # shallow / medium / deep

    system_message = """
    You are SmartBot Unified AI — a smart money & whales analysis engine.

    You analyze:
    - Whale accumulation and distribution
    - Liquidity zones
    - Order flow behavior (conceptual)
    - Market manipulation patterns
    - Smart money footprints

    Rules:
    - Identify asset type automatically if not specified.
    - Provide realistic, conservative insights.
    - Explain how whales could impact price.
    - Always include risk warnings.
    """

    prompt = f"""
    Perform a whales / smart money analysis with the following parameters:

    Asset: {asset or "Not specified"}
    Market: {market}
    Timeframe: {timeframe}
    Analysis depth: {depth}

    Please provide:
    1) Current whale activity (Accumulation / Distribution / Neutral)
    2) Liquidity zones (buy-side / sell-side)
    3) Likely manipulation scenarios (if any)
    4) Impact on short-term and medium-term price
    5) Retail trader risk
    6) Suggested action (Buy / Hold / Sell / Wait)
    """

    ai_reply = ai_chat(prompt, system_msg=system_message)

    return jsonify({
        "status": "success",
        "whales_analysis": ai_reply
    })
