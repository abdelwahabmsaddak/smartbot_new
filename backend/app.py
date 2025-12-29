import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)

# ===============================
# Public pages
# ===============================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ===============================
# Auth
# ===============================

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


# ===============================
# Dashboard & User
# ===============================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/usage")
def usage():
    return render_template("usage.html")


# ===============================
# Trading & AI
# ===============================

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/ai-signals")
def ai_signals():
    return render_template("ai_signals.html")

@app.route("/autotrade")
def autotrade():
    return render_template("autotrade.html")

@app.route("/auto-trading-pro")
def auto_trading_pro():
    return render_template("auto_trading_pro.html")

@app.route("/market-screener")
def market_screener():
    return render_template("market_screener.html")

@app.route("/whales")
def whales():
    return render_template("whales.html")


# ===============================
# History & Notifications
# ===============================

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/notifications")
def notifications():
    return render_template("notifications.html")


# ===============================
# Subscription & Payments
# ===============================

@app.route("/subscription")
def subscription():
    return render_template("subscription.html")

@app.route("/withdraw")
def withdraw():
    return render_template("withdraw.html")


# ===============================
# Chat
# ===============================

@app.route("/chat")
def chat():
    return render_template("chatbot_trader.html")

@app.route("/chat-widget")
def chat_widget():
    return render_template("chat_widget.html")


# ===============================
# Health (Render)
# ===============================

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
