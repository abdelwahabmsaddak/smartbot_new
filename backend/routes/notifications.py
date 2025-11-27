from flask import Blueprint, render_template, session
import sqlite3

notifications_bp = Blueprint("notifications", __name__)

def get_user_notifications(user_id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC",
                (user_id,))
    data = cur.fetchall()
    conn.close()
    return data


@notifications_bp.route("/notifications")
def notifications_page():
    user_id = session.get("user_id")
    data = get_user_notifications(user_id)
    return render_template("notifications.html", notifications=data)


def add_notification(user_id, type, message):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO notifications (user_id, type, message) VALUES (?, ?, ?)",
                (user_id, type, message))
    conn.commit()
    conn.close()
