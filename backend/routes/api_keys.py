from flask import Blueprint, request, jsonify
from utils.crypto import encrypt
from db import get_db

api_keys_bp = Blueprint("api_keys", __name__)

@api_keys_bp.route("/api/api_keys", methods=["POST"])
def save_api_keys():
    data = request.json
    user_id = data["user_id"]
    exchange = data["exchange"]
    api_key = encrypt(data["api_key"])
    api_secret = encrypt(data["api_secret"])

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO api_keys (user_id, exchange, api_key_encrypted, api_secret_encrypted)
        VALUES (?, ?, ?, ?)
    """, (user_id, exchange, api_key, api_secret))
    db.commit()

    return jsonify({"status": "saved"})
