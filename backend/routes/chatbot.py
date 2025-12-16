from flask import Blueprint, request, jsonify
from backend.services.ai_client import get_ai_client

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api")

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message required"}), 400

        client = get_ai_client()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
