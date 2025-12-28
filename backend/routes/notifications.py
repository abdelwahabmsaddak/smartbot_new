from flask import Blueprint, jsonify, session
from db import get_db

bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

@bp.route("", methods=["GET"])
def get_notifications():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])

    db = get_db()
    rows = db.execute("""
        SELECT id, title, message, type, is_read, created_at
        FROM notifications
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 20
    """, (user_id,)).fetchall()

    return jsonify([dict(row) for row in rows])
