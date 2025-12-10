from flask import Blueprint, render_template, request, jsonify
from backend.db import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    affiliates = db.execute("SELECT * FROM affiliates").fetchall()
    withdrawals = db.execute("SELECT * FROM withdrawals").fetchall()

    return render_template(
        'admin/dashboard.html',
        users=users,
        affiliates=affiliates,
        withdrawals=withdrawals
    )

@admin_bp.route('/update_plan', methods=['POST'])
def update_plan():
    db = get_db()
    user_id = request.json['user_id']
    plan = request.json['plan']
    db.execute("UPDATE users SET plan=? WHERE id=?", (plan, user_id))
    db.commit()
    return jsonify({"success": True})

@admin_bp.route('/approve_withdraw', methods=['POST'])
def approve_withdraw():
    db = get_db()
    wid = request.json['withdraw_id']
    db.execute("UPDATE withdrawals SET status='approved' WHERE id=?", (wid,))
    db.commit()
    return jsonify({"success": True})
