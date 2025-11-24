from flask import Blueprint, render_template, request, session, redirect
import sqlite3
import datetime

withdraw_bp = Blueprint('withdraw_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@withdraw_bp.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db()
    cur = conn.cursor()

    # مجموع الأرباح
    cur.execute("SELECT SUM(amount) as total FROM affiliate_earnings WHERE user_id=?", (user_id,))
    total = cur.fetchone()['total'] or 0

    if request.method == 'POST':
        amount = float(request.form['amount'])
        wallet = request.form['wallet']

        # تسجيل طلب السحب
        cur.execute("""
            INSERT INTO withdrawals (user_id, amount, wallet, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, amount, wallet, "pending", datetime.datetime.now()))

        conn.commit()

        return "✔ تم إرسال طلب السحب بنجاح"

    return render_template("withdraw.html", total=total)
