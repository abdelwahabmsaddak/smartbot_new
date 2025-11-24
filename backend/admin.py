from flask import Blueprint, render_template, session, redirect
import sqlite3

admin_bp = Blueprint('admin_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/admin/users')
def users_page():
    if 'user_id' not in session or session.get("is_admin") != 1:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()

    return render_template("users.html", users=users)
@admin_bp.route('/admin')
def admin_home():
    if 'user_id' not in session or session.get("is_admin") != 1:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as c FROM users")
    users_count = cursor.fetchone()['c']

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template("admin_dashboard.html",
                           users=users,
                           users_count=users_count,
                           plans_count=0)
