from flask import Flask
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.payments import payments_bp
from database import init_db
def create_users_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
app = Flask(__name__)
app.secret_key = "SECRET_KEY"

# تهيئة قاعدة البيانات (إنشاء جدول الأدمن + المستخدمين)
init_db()

# تسجيل البلوبربنت
app.register_blueprint(auth_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(payments_bp)

@app.route('/')
def home():
    return "Server is running..."

if __name__ == '__main__':
    app.run(debug=True)
@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('dashboard.html')
