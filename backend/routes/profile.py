from flask import Blueprint, render_template, request, session, redirect
import sqlite3

profile_bp = Blueprint('profile_bp', __name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    user_id = session['user_id']

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if password.strip() == "":
            cursor.execute(
                "UPDATE users SET username=?, email=? WHERE id=?",
                (username, email, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET username=?, email=?, password=? WHERE id=?",
                (username, email, password, user_id)
            )

        conn.commit()
        return redirect('/profile')

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    return render_template("profile.html", user=user)
