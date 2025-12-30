import os
from flask import Flask, render_template, request, redirect, url_for, session

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "smartbot_secret_key"


# =====================
# ROUTES
# =====================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("email", "user")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("login"))
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


@app.route("/market-screener")
def market_screener():
    return render_template("market_screener.html")


@app.route("/whales")
def whales():
    return render_template("whales.html")


@app.route("/usage")
def usage():
    return render_template("usage.html")


@app.route("/subscription")
def subscription():
    return render_template("subscription.html")


@app.route("/withdraw")
def withdraw():
    return render_template("withdraw.html")


@app.route("/chat")
def chat():
    return render_template("chat_widget.html")


# =====================
# RUN
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
