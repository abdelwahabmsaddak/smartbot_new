from flask import Blueprint, request, jsonify
from backend.ai_core import chat_answer

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    user_id = data.get("user_id")

    if not message:
        return jsonify({"reply": "❗ Please type a message."})

    reply = chat_answer(message, user_id=user_id)
    return jsonify({"reply": reply})
