   from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

analysis_bp = Blueprint("analysis_bp", __name__)

@analysis_bp.route("/analysis", methods=["POST"])
def ai_analysis():
    """
    Route تحليل ذكي موحّد:
    - Crypto
    - Gold
    - Halal Stocks
    """
    data = request.get_json() or {}

    # مدخلات المستخدم
    asset = data.get("asset", "")          # مثال: BTC, GOLD, ARAMCO
    market = data.get("market", "auto")    # crypto / gold / stock / auto
    horizon = data.get("horizon", "medium")# short / medium / long
    focus = data.get("focus", "general")   # risk / halal / fundamentals / technical

    # برومبت احترافي
    system_message = """
    You are SmartBot Unified AI for financial analysis.
    You analyze:
    - Cryptocurrencies
    - Gold & precious metals
    - Halal (Sharia-compliant) stocks

    You must:
    - Identify the asset type automatically if not specified.
    - For stocks: determine if Halal or Haram and explain why.
    - Provide technical + fundamental insights.
    - Give Buy/Hold/Sell recommendation.
    - Provide risk level (Low/Medium/High).
    - Give short, medium, and long-term outlooks.
    - Explain clearly and concisely.
    """

    prompt = f"""
    Analyze the following asset:

    Asset: {asset or "Not specified"}
    Market: {market}
    Investment horizon: {horizon}
    Focus: {focus}

    Please provide:
    1) Asset classification (Crypto / Gold / Halal Stock)
    2) Halal status (if stock)
    3) Key drivers and risks
    4) Technical outlook
    5) Fundamental outlook
    6) Recommendation (Buy/Hold/Sell)
    7) Risk level
    8) Price targets (if applicable)
    """

    ai_reply = ai_chat(prompt, system_msg=system_message)

    return jsonify({
        "status": "success",
        "analysis": ai_reply
    })    
