from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

ai_trader_bp = Blueprint("ai_trader_bp", __name__)

@ai_trader_bp.route("/trader", methods=["POST"])
def ai_trader():
    """
    خطة تداول ذكية موحّدة:
    - Crypto
    - Gold
    - Halal Stocks
    """
    data = request.get_json() or {}

    asset = data.get("asset", "")                 # BTC, ETH, GOLD, ARAMCO
    market = data.get("market", "auto")           # crypto / gold / stock / auto
    capital = data.get("capital", 1000)           # رأس المال
    risk_per_trade = data.get("risk_per_trade", 1)# % المخاطرة في الصفقة
    timeframe = data.get("timeframe", "4H")       # الإطار الزمني
    style = data.get("style", "swing")            # scalp / day / swing / position

    system_message = """
    You are SmartBot Unified AI — a professional trading strategist.

    You build complete trading plans for:
    - Cryptocurrencies
    - Gold & precious metals
    - Halal (Sharia-compliant) stocks

    Rules:
    - Identify asset type automatically if not specified.
    - For stocks: ensure Sharia compliance.
    - Build a full trading plan including:
        * Market bias
        * Strategy description
        * Entry logic
        * Take-profit targets
        * Stop-loss
        * Position sizing based on capital and risk
        * Risk management rules
    - Be realistic and conservative.
    """

    prompt = f"""
    Build a complete trading plan with the following parameters:

    Asset: {asset or "Not specified"}
    Market: {market}
    Capital: {capital}
    Risk per trade (%): {risk_per_trade}
    Timeframe: {timeframe}
    Trading style: {style}

    Please include:
    1) Market bias (Bullish / Bearish / Range)
    2) Strategy overview
    3) Entry rules
    4) Take-profit targets
    5) Stop-loss
    6) Position size calculation
    7) Risk-reward ratio
    8) Alternative scenario
    """

    ai_reply = ai_chat(prompt, system_msg=system_message)

    return jsonify({
        "status": "success",
        "trading_plan": ai_reply
    })
