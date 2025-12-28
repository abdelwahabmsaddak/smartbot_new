from db import get_db

def create_notification(user_id, title, message, type="system"):
    db = get_db()
    db.execute("""
        INSERT INTO notifications (user_id, title, message, type)
        VALUES (?, ?, ?, ?)
    """, (user_id, title, message, type))
    db.commit()
