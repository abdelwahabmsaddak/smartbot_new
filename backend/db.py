
import sqlite3

# ==========================
# INITIAL DATABASE CREATION
# ==========================

def create_posts_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_notifications_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read INTEGER DEFAULT 0
        );
    """)

    conn.commit()
    conn.close()


def create_users_table():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==========================
# RUN ALL TABLE CREATIONS
# ==========================
create_posts_table()
create_notifications_table()
create_users_table()    
