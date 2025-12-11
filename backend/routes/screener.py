from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

screener_bp = Blueprint("screener_bp", __name__)

@screener_bp.route("/screener", methods=["POST"])
def ai_screener():
    """
    سكرينر ذكي يعتمد كليًا على الذكاء الاصطناعي.
    يعطي:
    - أفضل عملات اليوم
    - ترند السوق
    - تحليل صعود/هبوط
    -Coins to watch
    - توصيات شراء/بيع
    """

    data = request.get_json()

    user_request = data.get("type", "general")  # user may specify: 'daily', 'top', 'trend', 'meme'

    system_message = """
    You are SmartBot AI - a professional crypto screener.
    Your tasks:
    - Analyze the entire crypto market.
    - List top performing coins.
    - Identify trending coins.
    - Detect meme coins that may pump.
    - Give buy/sell recommendations.
    - Provide percentage predictions.
    - Provide reasoning behind every suggestion.
    Always return structured data.
    """

    # نركّب برومبت واضح لي AI
    prompt = f"""
    User request: {user_request}

    Provide:
    - Top 5 performing crypto coins
    - Top 5 trending meme coins
    - Today’s market sentiment (Bullish / Bearish)
    - Recommendations (Buy / Hold / Sell)
    - Targets and risk level
    """

    ai_reply = ai_chat(prompt, system_msg=system_message)

    return jsonify({
        "status": "success",
        "analysis": ai_reply
    })
