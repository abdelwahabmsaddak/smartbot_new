from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

chatbot_bp = Blueprint("chatbot_bp", __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def smart_chatbot():
    """
    شات بوت كامل يعتمد على الذكاء الاصطناعي.
    يفهم أي سؤال: تداول، برمجة، تحليل مشاريع، نصائح، ذكاء اصطناعي...
    """

    data = request.get_json()

    # التحقق من وجود الرسالة
    if not data or "message" not in data:
        return jsonify({"error": "Message field is required"}), 400

    user_msg = data["message"]

    # صياغة برومبت احترافي يضمن أقصى ذكاء ممكن
    system_message = """
    You are SmartBot AI.
    You specialize in:
    - Crypto trading
    - Market analysis
    - Project evaluation
    - Investment recommendations
    - Technical analysis
    - Meme coins predictions
    - Python code writing
    - Debugging
    - Personal finance
    - General knowledge

    Respond clearly and powerfully.
    If the user asks for analysis, give numbers.
    If the user asks for trading advice, give strategies.
    If the user asks programming, return clean code.
    """

    ai_reply = ai_chat(user_msg, system_msg=system_message)

    return jsonify({
        "status": "success",
        "reply": ai_reply
    })
