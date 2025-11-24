from flask import Blueprint, request, jsonify, session, redirect
import sqlite3
import openai
import json

chatbot_bp = Blueprint('chatbot_bp', __name__)

# إعداد OpenAI API
openai.api_key = "ضع_مفتاحك_هنا"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        # طلب API من OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response['choices'][0]['message']['content']
        tokens_used = response['usage']['total_tokens']

        # حفظ الاستخدام في قاعدة البيانات
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usage (user_id, tokens_used) VALUES (?, ?)",
            (session['user_id'], tokens_used)
        )
        conn.commit()

        return jsonify({
            "reply": bot_reply,
            "tokens_used": tokens_used
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
