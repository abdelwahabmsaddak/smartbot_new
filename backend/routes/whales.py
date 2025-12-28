from flask import Blueprint, jsonify
from db import get_db

bp = Blueprint("whales", __name__, url_prefix="/api/whales")

@bp.route("", methods=["GET"])
def get_whales():
    db = get_db()
    rows = db.execute("""
        SELECT asset, amount, direction, exchange, created_at
        FROM whale_alerts
        ORDER BY created_at DESC
        LIMIT 20
    """).fetchall()

    return jsonify([dict(row) for row in rows])
