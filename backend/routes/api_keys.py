from flask import Blueprint, request, jsonify, session
import sqlite3

api_keys_bp = Blueprint("api_keys", __name__)

def get_db():
    return sqlite3.connect("database.db", check_same_thread=False)

@api_keys_bp.route("/api/save_keys", methods=["POST"])
def save_keys():
    if "user_id" not in session:
        return jsonify({"error": "not logged in"})

    data = request.json
    user = session["user_id"]

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO api_keys(user_id, binance_key, binance_secret,
                                        okx_key, okx_secret,
                                        kucoin_key, kucoin_secret)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user,
        data.get("binance_key"),
        data.get("binance_secret"),
        data.get("okx_key"),
        data.get("okx_secret"),
        data.get("kucoin_key"),
        data.get("kucoin_secret")
    ))

    db.commit()
    return jsonify({"status": "success"})
