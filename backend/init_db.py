import sqlite3

# =======================
# CONNECT TO DATABASE
# =======================
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# =======================
# CREATE TABLES
# =======================

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS affiliate_earnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    source_user INTEGER,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan TEXT,
    status TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    wallet TEXT,
    status TEXT,
    created_at TEXT
)
""")

# =======================
# SAVE AND CLOSE
# =======================
conn.commit()
conn.close()

print("Database initialized successfully.")
