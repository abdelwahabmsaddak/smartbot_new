from flask import Flask, render_template, redirect, session
from auth import auth_bp
from routes.admin import admin_bp
from routes.profile import profile_bp
from routes.usage import usage_bp
from routes.chatbot import chatbot_bp
from routes.payments import payments_bp        # إن وجد
from routes.billing import billing_bp          # إن وجد
from routes.affiliate import affiliate_bp      # صفحة الافلييت
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from flask import Blueprint, request, jsonify
import requests
import talib
import numpy as np
from backend.auto_trading import AutoTradingEngine, StrategyConfig, TradingMode, DummyExchange
from flask import Flask, jsonify
import requests
import time
from routes.auto_trading_pro import auto_trading_pro_bp
from routes.screener import screener_bp
from routes.multi_trading import multi_bp
from routes.api_keys import api_keys_bp
from flask import session
from backend.languages import translate
from routes.settings import settings_bp
app.register_blueprint(settings_bp)

@app.context_processor
def inject_translator():
    lang = session.get("lang", "en")
    return {"t": lambda key: translate(lang, key)}

@app.get("/api_keys")
def api_keys_page():
    return render_template("api_keys.html")
app.register_blueprint(api_keys_bp)
app.register_blueprint(multi_bp)
app.register_blueprint(screener_bp)
app.register_blueprint(auto_trading_pro_bp)
app = Flask(__name__)
@app.get("/set_lang/<lang>")
def set_lang(lang):
    session["lang"] = lang
    return redirect(request.headers.get("Referer", "/dashboard"))
    
# مثال API واحد – ويمكن تغييرها لأي منصة
WHALE_API = "https://api.whale-alert.io/v1/transactions?api_key=YOUR_KEY"

@app.get("/api/whales")
def whales():
    # مثال (بيانات وهمية بدون API Key)
    sample = [
        {
            "symbol": "BTC",
            "amount": "350 BTC",
            "from": "محفظة غير معروفة",
            "to": "Binance",
            "time": time.strftime("%Y-%m-%d %H:%M")
        },
        {
            "symbol": "ETH",
            "amount": "12,000 ETH",
            "from": "Coinbase",
            "to": "محفظة حوت",
            "time": time.strftime("%Y-%m-%d %H:%M")
        }
    ]
    return jsonify(sample)
engine = AutoTradingEngine()

# مثال: تسجيل منصة عامة (تستبدل DummyExchange لاحقاً بـ BinanceClient أو BybitClient إلخ)
engine.register_exchange_client(
    "binance",
    DummyExchange(api_key="XXX", api_secret="YYY", name="binance")
)

# عند التسجيل أو من لوحة الإعدادات:
config = StrategyConfig(
    user_id=1,
    mode=TradingMode.FULL_AUTO,          # أو SEMI_AUTO أو SIGNALS_ONLY
    max_risk_per_trade_pct=1.0,
    max_daily_loss_pct=5.0,
    max_positions=3,
    symbols=["BTCUSDT", "XAUUSD", "AAPL"],  # عملات + ذهب + أسهم
    exchanges=["binance"],               # لاحقاً تضيف "bybit", "okx" ...
    use_smart_analysis=True,
    auto_trading_enabled=True,
)
engine.set_user_strategy(config)

@analysis_bp.route("/analysis_api", methods=["POST"])
def analysis_api():
    data = request.json
    symbol = data["symbol"]
    indicators = data["indicators"]

    # مثال: نجيب البيانات من Binance
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=200"
    candles = requests.get(url).json()

    close_prices = np.array([float(c[4]) for c in candles])
    volume = np.array([float(c[5]) for c in candles])

    result = {}

    if "ma" in indicators:
        result["MA20"] = float(talib.SMA(close_prices, 20)[-1])

    if "ema" in indicators:
        result["EMA12"] = float(talib.EMA(close_prices, 12)[-1])

    if "macd" in indicators:
        macd, signal, hist = talib.MACD(close_prices)
        result["MACD"] = {
            "macd": float(macd[-1]),
            "signal": float(signal[-1]),
            "histogram": float(hist[-1])
        }

    if "rsi" in indicators:
        result["RSI"] = float(talib.RSI(close_prices, 14)[-1])

    if "volume" in indicators:
        result["Volume"] = float(volume[-1])

    if "support" in indicators:
        result["Support"] = float(min(close_prices[-20:]))
        result["Resistance"] = float(max(close_prices[-20:]))

    if "whales" in indicators:
        result["Whale_Alert"] = "🚨 سيتم إضافة API لاحقًا للحيتان"

    return jsonify(result)
app = Flask(__name__)

# === عرض إدارة المدونة ===
@app.route("/admin/blog")
def admin_blog():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("admin_blog.html", posts=posts)


# === إنشاء مقال ===
@app.route("/admin/blog/create", methods=["POST"])
def create_post():
    title = request.form["title"]
    content = request.form["content"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
              (title, content, now, now))
    conn.commit()
    conn.close()

    return redirect("/admin/blog")


# === تعديل مقال ===
@app.route("/admin/blog/edit/<int:id>")
def edit_post(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (id,))
    post = c.fetchone()
    conn.close()
    return render_template("edit_post.html", post=post)


@app.route("/admin/blog/edit/<int:id>", methods=["POST"])
def save_edit_post(id):
    title = request.form["title"]
    content = request.form["content"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET title=?, content=?, updated_at=? WHERE id=?",
              (title, content, now, id))
    conn.commit()
    conn.close()

    return redirect("/admin/blog")


# === حذف مقال ===
@app.route("/admin/blog/delete/<int:id>")
def delete_post(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin/blog")
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
