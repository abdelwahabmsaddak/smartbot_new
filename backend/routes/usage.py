from flask import Blueprint, render_template, session, redirect
import sqlite3

usage_bp = Blueprint('usage_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@usage_bp.route('/usage')
def usage():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    # جلب مفتاح API للمستخدم
    cursor.execute("SELECT api_key FROM users WHERE id=?", (session['user_id'],))
    api_key = cursor.fetchone()['api_key']

    # جلب بيانات الاستهلاك
    cursor.execute("""
        SELECT day, requests FROM usage_logs
        WHERE user_id=?
        ORDER BY day DESC
        LIMIT 30
    """, (session['user_id'],))

    usage_data = cursor.fetchall()

    return render_template("usage.html", api_key=api_key, usage=usage_data)
