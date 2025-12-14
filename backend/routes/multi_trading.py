from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

multi_trading_bp = Blueprint("multi_trading_bp", __name__)

@multi_trading_bp.route("/multi_trading", methods=["POST"])
def multi_trading():
    """
    محفظة متعددة الأصول (Crypto + Gold + Halal Stocks) بالذكاء الاصطناعي.
    """
    data = request.get_json() or {}

    capital = data.get("capital", 1000)
    risk_profile = data.get("risk", "medium")         # low / medium / high
    horizon = data.get("horizon", "medium")           # short / medium / long
    preferences = data.get("preferences", [])         # مثال: ["meme_coins", "gold_safe", "dividend_stocks"]
    halal_strict = data.get("halal_strict", True)     # فلترة الأسهم الحلال

    system_message = """
    You are SmartBot Unified AI — a portfolio & multi-asset allocation engine.

    You build investment portfolios across:
    - Cryptocurrency
    - Gold & precious metals
    - Halal (Sharia-compliant) stocks

    Rules:
    - If halal_strict is true, only include Sharia-compliant stocks.
    - Provide a clear allocation plan (percentages + amounts).
    - Include risk controls and rebalancing schedule.
    - Provide reasoning for each allocation.
    - Be realistic and conservative.
    """

    prompt = f"""
    Build a multi-asset portfolio plan with:

    Capital: {capital}
    Risk profile: {risk_profile}
    Investment horizon: {horizon}
    Preferences: {preferences}
    Halal strict: {halal_strict}

    Provide:
    1) Allocation between Crypto / Gold / Halal Stocks (percent + amount)
    2) Suggested assets in each category (examples)
    3) Strategy for each category (entry style)
    4) Risk management rules
    5) Rebalancing schedule (weekly/monthly/quarterly)
    6) What to avoid (common mistakes)
    """

    ai_reply = ai_chat(prompt, system_msg=system_message)

    return jsonify({
        "status": "success",
        "portfolio_plan": ai_reply
    })
