from flask import Blueprint, jsonify, session
from db import get_db

bp = Blueprint("history", __name__, url_prefix="/api/history")

@bp.route("", methods=["GET"])
def get_history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])

    db = get_db()
    rows = db.execute("""
        SELECT asset, asset_type, signal, confidence, created_at
        FROM history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 50
    """, (user_id,)).fetchall()

    return jsonify([dict(row) for row in rows])
