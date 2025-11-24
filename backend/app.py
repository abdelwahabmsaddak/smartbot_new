from flask import Flask, render_template, redirect, session
from auth import auth_bp
from routes.admin import admin_bp
from routes.profile import profile_bp
from routes.usage import usage_bp
from routes.chatbot import chatbot_bp
from routes.payments import payments_bp        # إن وجد
from routes.billing import billing_bp          # إن وجد
from routes.affiliate import affiliate_bp      # صفحة الافلييت

app = Flask(__name__)
app.secret_key = "SECRET_KEY"   # بدّلها فيما بعد


# ==============================
# 📌 تسجيل جميع البلوبرنت
# ==============================

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(usage_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(affiliate_bp)

# لو عندك payments و billing
try:
    app.register_blueprint(payments_bp)
    app.register_blueprint(billing_bp)
except:
    pass


# ==============================
# 📌 الروت الرئيسي — الصفحة الرئيسية
# ==============================

@app.route('/')
def home():
    return render_template('index.html')


# ==============================
# 📌 الداشبورد للمستخدم بعد الدخول
# ==============================

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')


# ==============================
# 📌 تشغيل السيرفر
# ==============================

if __name__ == '__main__':
    app.run(debug=True)
