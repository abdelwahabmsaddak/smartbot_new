from flask import Flask, render_template, redirect, session
from auth import auth_bp
from routes.admin import admin_bp
from routes.profile import profile_bp
from routes.usage import usage_bp
from routes.chatbot import chatbot_bp
from routes.payments import payments_bp
from routes.billing import billing_bp
from routes.affiliate import affiliate_bp
from routes.settings import settings_bp
from routes.api_keys import api_keys_bp
from routes.ai_trader import ai_trader_bp
from routes.whales import whales_bp
from routes.screener import screener_bp
from routes.auto_trading import auto_bp
from routes.multi_trading import multi_bp

from config import OPENAI_API_KEY
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "secret-key"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(usage_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(affiliate_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(ai_trader_bp)
app.register_blueprint(whales_bp)
app.register_blueprint(screener_bp)
app.register_blueprint(auto_bp)
app.register_blueprint(multi_bp)

client = OpenAI(api_key=OPENAI_API_KEY)

# ===========================
# الصفحة الرئيسية
# ===========================
@app.route('/')
def home():
    return render_template('index.html')

# ===========================
# الداشبورد
# ===========================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

# ===========================
# تشغيل السيرفر
# ===========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
