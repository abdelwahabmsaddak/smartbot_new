import ccxt
from flask import Blueprint, request, jsonify
from utils.crypto import decrypt
from db import get_db

auto_trading_pro_bp = Blueprint("auto_trading_pro", __name__)

@auto_trading_pro_bp.route("/api/auto_trading_pro", methods=["POST"])
def auto_trading_pro():
    data = request.json

    if data["mode"] != "live":
        return jsonify({"error": "Only live mode here"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT exchange, api_key_encrypted, api_secret_encrypted FROM api_keys WHERE id = ?",
                (data["api_key_id"],))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "API key not found"}), 404

    exchange_name, enc_key, enc_secret = row
    api_key = decrypt(enc_key)
    api_secret = decrypt(enc_secret)

    exchange = getattr(ccxt, exchange_name)({
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True
    })

    order = exchange.create_order(
        symbol=data["symbol"],
        type=data["type"],
        side=data["side"],
        amount=data["quantity"]
    )

    return jsonify({
        "status": "executed",
        "order": order
    })
