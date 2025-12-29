import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# ==============================
# App init
# ==============================
app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# ==============================
# Basic home (IMPORTANT)
# ==============================
@app.route("/")
def home():
    return "SmartBot backend is running 🚀"

# ==============================
# Health check (Render friendly)
# ==============================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ==============================
# Chat API (SAFE VERSION)
# ==============================
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    question = data.get("message", "").strip()

    if not question:
        return jsonify({
            "answer": "❌ Please send a message"
        })

    # 🔹 TEMP answer (AI logic نربطوها بعد)
    answer = (
        "🤖 SmartBot (Demo)\n\n"
        f"سؤالك: {question}\n\n"
        "✅ Backend شغّال\n"
        "⚙️ AI logic يتربط في المرحلة الجاية"
    )

    return jsonify({
        "answer": answer
    })

# ==============================
# Run (Render compatible)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
