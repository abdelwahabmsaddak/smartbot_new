# routes/affiliate.py
from flask import Blueprint, render_template, session, redirect
import sqlite3
from flask import Blueprint, render_template, session, redirect
import sqlite3

affiliate_bp = Blueprint('affiliate_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@affiliate_bp.route('/affiliate-stats')
def affiliate_stats():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db()
    cur = conn.cursor()

    # عدد الإحالات
    cur.execute("SELECT COUNT(*) AS total_refs FROM users WHERE referred_by=?", (user_id,))
    referrals = cur.fetchone()['total_refs']

    # الأرباح
    cur.execute("SELECT COALESCE(SUM(amount),0) AS total_earn FROM affiliate_earnings WHERE user_id=?", (user_id,))
    total_earn = cur.fetchone()['total_earn']

    # قائمة الإحالات بالتفصيل
    cur.execute("SELECT id, email, created_at FROM users WHERE referred_by=?", (user_id,))
    referrals_list = cur.fetchall()

    # قائمة الأرباح بالتفصيل
    cur.execute("SELECT amount, source_user, created_at FROM affiliate_earnings WHERE user_id=?", (user_id,))
    earnings_list = cur.fetchall()

    return render_template(
        "affiliate_stats.html",
        referrals=referrals,
        total_earn=total_earn,
        referrals_list=referrals_list,
        earnings_list=earnings_list,
    )
affiliate_bp = Blueprint("affiliate_bp", __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@affiliate_bp.route("/affiliate")
def affiliate_page():
    # التحقق من أن المستخدم مسجل دخول
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()

    # جلب الأرباح
    cur.execute("SELECT SUM(amount) AS total FROM affiliate_earnings WHERE user_id=?", (user_id,))
    total = cur.fetchone()["total"]
    if total is None:
        total = 0

    # عدد الأشخاص الذين سجلوا من رابطك
    cur.execute("SELECT COUNT(*) AS count FROM users WHERE referred_by=?", (user_id,))
    ref_count = cur.fetchone()["count"]

    # رابط الإحالة
    referral_link = f"https://yourwebsite.com/signup?ref={user_id}"

    conn.close()

    return render_template("affiliate.html",
                           total_earnings=total,
                           referrals=ref_count,
                           referral_link=referral_link)
