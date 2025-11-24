from flask import Blueprint, render_template, session, redirect
import sqlite3

affiliate_bp = Blueprint('affiliate_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@affiliate_bp.route('/affiliate')
def affiliate_page():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db()
    cur = conn.cursor()

    # رابط الإحالة
    referral_link = f"https://smartbot.com/signup?ref={user_id}"

    # إجمالي الأرباح
    cur.execute("SELECT SUM(amount) as total FROM affiliate_earnings WHERE user_id=?", (user_id,))
    total_earnings = cur.fetchone()['total'] or 0

    # عدد الإحالات
    cur.execute("SELECT COUNT(*) as cnt FROM users WHERE referred_by=?", (user_id,))
    total_referrals = cur.fetchone()['cnt']

    # تفاصيل الأرباح
    cur.execute("SELECT * FROM affiliate_earnings WHERE user_id=? ORDER BY id DESC", (user_id,))
    earnings = cur.fetchall()

    return render_template('affiliate.html',
                           referral_link=referral_link,
                           total_earnings=total_earnings,
                           total_referrals=total_referrals,
                           earnings=earnings)
