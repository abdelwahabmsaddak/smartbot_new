from flask import Blueprint, render_template, request, session
from database import get_db

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings")
def settings_page():
    db = get_db()
    cur = db.execute("SELECT * FROM api_keys WHERE user_id=?", (session["user_id"],))
    api = cur.fetchone()
    return render_template("settings.html", api=api)

@settings_bp.route("/save_api_keys", methods=["POST"])
def save_api_keys():
    db = get_db()

    db.execute("""
        INSERT INTO api_keys 
        (user_id, binance_key, binance_secret, bybit_key, bybit_secret, whale_key, telegram_token, telegram_chat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        binance_key=excluded.binance_key,
        binance_secret=excluded.binance_secret,
        bybit_key=excluded.bybit_key,
        bybit_secret=excluded.bybit_secret,
        whale_key=excluded.whale_key,
        telegram_token=excluded.telegram_token,
        telegram_chat=excluded.telegram_chat
    """, (
        session["user_id"],
        request.form["binance_key"],
        request.form["binance_secret"],
        request.form["bybit_key"],
        request.form["bybit_secret"],
        request.form["whale_key"],
        request.form["telegram_token"],
        request.form["telegram_chat"]
    ))

    db.commit()
    return "تم الحفظ بنجاح ✔️"
