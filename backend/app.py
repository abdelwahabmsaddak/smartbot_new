# =========================================
# SmartBot Backend App
# =========================================

import os
import importlib
from flask import Flask, request, jsonify, session
from flask_cors import CORS

# AI Core
from backend.ai_core import chat_answer

# =========================================
# Paths (مهم جدا)
# =========================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
ROUTES_DIR = os.path.join(BASE_DIR, "routes")

# =========================================
# Flask App
# =========================================

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = os.environ.get("SECRET_KEY", "smartbot-secret-key")
CORS(app)

# =========================================
# API — Chat
# =========================================

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Main AI Chat endpoint
    """
    data = request.json or {}
    question = data.get("message", "").strip()

    if not question:
        return jsonify({
            "answer": "❗ Please type a question."
        })

    user_id = session.get("user_id")
    is_guest = user_id is None

    try:
        answer = chat_answer(
            question=question,
            user_id=user_id,
            guest=is_guest
        )

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "answer": "⚠️ Something went wrong. Try again later."
        }), 500

# =========================================
# Auto-register Blueprints
# =========================================

def register_all_blueprints():
    if not os.path.exists(ROUTES_DIR):
        print("⚠️ routes folder not found")
        return

    for filename in os.listdir(ROUTES_DIR):
        if not filename.endswith(".py") or filename.startswith("_"):
            continue

        module_name = filename[:-3]
        module_path = f"backend.routes.{module_name}"

        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"❌ Failed to load {module_path}: {e}")
            continue

        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            try:
                from flask import Blueprint
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
                    print(f"✅ Blueprint registered: {attr.name}")
            except Exception as e:
                print(f"❌ Blueprint error in {module_name}: {e}")

# =========================================
# Health Check
# =========================================

@app.route("/health")
def health():
    return {"status": "ok"}

# =========================================
# Init
# =========================================

register_all_blueprints()

# =========================================
# Run (Render compatible)
# =========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
