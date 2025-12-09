import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    user_id INTEGER PRIMARY KEY,
    binance_key TEXT,
    binance_secret TEXT,
    bybit_key TEXT,
    bybit_secret TEXT,
    whale_key TEXT,
    telegram_token TEXT,
    telegram_chat TEXT
)
""")

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
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM admin")  # optional

cursor.execute("""
INSERT INTO admin (username, password)
VALUES ('admin', 'admin123')
""")

conn.commit()
# جدول أرباح الأفلييت
cur.execute("""
CREATE TABLE IF NOT EXISTS affiliate_earnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    source_user INTEGER,
    created_at TEXT
)
""")

# جدول الاشتراكات
cur.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan TEXT,
    status TEXT,
    created_at TEXT
)
""")

# جدول السحوبات
cur.execute("""
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    wallet TEXT,
    status TEXT,
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Admin user created.")
