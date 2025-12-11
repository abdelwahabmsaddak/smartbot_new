from flask import Blueprint, request, jsonify
from backend.ai_core import ai_chat  # دالة الذكاء الاصطناعي الخاصة بك
import sqlite3

chatbot_bp = Blueprint('chatbot_bp', __name__, url_prefix="/chatbot")


# ---------------------------
#  GET DATABASE CONNECTION
# ---------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
#  CHATBOT ENDPOINT
# ---------------------------
@chatbot_bp.route('/ask', methods=['POST'])
def ask_bot():
    try:
        data = request.get_json()
        user_id = data.get("user_id", None)
        message = data.get("message", "")

        if not message.strip():
            return jsonify({"error": "Empty message"}), 400

        # الذكاء الاصطناعي
        bot_reply = ai_chat(message)

        # تسجيل المحادثة في الداتابايس
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (user_id, message, reply)
            VALUES (?, ?, ?)
        """, (user_id, message, bot_reply))

        conn.commit()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
