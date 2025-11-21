from flask import Flask
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.payments import payments_bp
from database import init_db

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
