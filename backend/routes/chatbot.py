from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat

chatbot_bp = Blueprint("chatbot_bp", __name__)


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_msg = data["message"]
    ai_reply = ai_chat(user_msg)

    return jsonify({"reply": ai_reply})
