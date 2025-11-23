from flask import Blueprint, request, render_template, redirect, session
import sqlite3

auth_bp = Blueprint('auth_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------
# REGISTER
# ------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            conn.commit()
            return redirect('/login')
        except:
            return render_template('register.html', error="المستخدم أو البريد موجود مسبقاً")

    return render_template('register.html')


# ------------------------
# LOGIN
# ------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')

        return render_template('login.html', error="خطأ في تسجيل الدخول")

    return render_template('login.html')
