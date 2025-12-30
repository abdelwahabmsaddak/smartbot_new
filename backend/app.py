import os
from flask import Flask, render_template, redirect, url_for

# =========================
# Base paths (مهم جدا)
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# =========================
# Flask app
# =========================
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = "smartbot_secret_key"

# =========================
# Pages routes
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/notifications")
def notifications():
    return render_template("notifications.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/subscription")
def subscription():
    return render_template("subscription.html")


@app.route("/usage")
def usage():
    return render_template("usage.html")


@app.route("/whales")
def whales():
    return render_template("whales.html")


@app.route("/withdraw")
def withdraw():
    return render_template("withdraw.html")


@app.route("/market")
def market():
    return render_template("market_screener.html")


@app.route("/chat")
def chat():
    return render_template("chatbot_trader.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


# =========================
# Health check (Render)
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}


# =========================
# Run (Render compatible)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
