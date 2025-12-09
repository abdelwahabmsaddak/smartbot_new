import sqlite3
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # جدول المستخدمين
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            plan TEXT DEFAULT 'free',
            join_date TEXT
        )
    """)

    # جدول الأفيليت
    c.execute("""
        CREATE TABLE IF NOT EXISTS affiliate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT UNIQUE,
            clicks INTEGER DEFAULT 0,
            signups INTEGER DEFAULT 0,
            earnings REAL DEFAULT 0
        )
    """)

    cur.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    user_id INTEGER PRIMARY KEY,
    binance_key TEXT,
    binance_secret TEXT,
    okx_key TEXT,
    okx_secret TEXT,
    kucoin_key TEXT,
    kucoin_secret TEXT
)
""")
    
    # جدول الأرباح
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            type TEXT,
            date TEXT
        )
    """)

    # جدول منشورات المدونة
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

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
    conn.commit()
    conn.close()
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def create_users_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTA
            MP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

create_users_table()
