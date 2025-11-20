import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# جدول المستخدمين
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    plan TEXT DEFAULT 'free',
    created_at TEXT,
    expired_at TEXT,
    is_admin INTEGER DEFAULT 0
)
""")

# جدول تسجيل الدخول
cur.execute("""
CREATE TABLE IF NOT EXISTS login_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    ip TEXT,
    device TEXT,
    date TEXT
)
""")

# جدول العمليات (للموقع)
cur.execute("""
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized.")
