from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .database import init_db
from .routes.auth import auth_bp
from .routes.api import api_bp
from .routes.payments import payments_bp  # نجهزه كستب لاحقة
from backend.routes import auth
app.include_router(auth.router)
from flask import Flask, request, jsonify
import sqlite3, datetime

app = Flask(__name__)

def db():
    return sqlite3.connect("database.db")

@app.post("/api/register")
def register():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    try:
        conn = db()
        cur = conn.cursor()

        # شهر مجاني
        now = datetime.datetime.now()
        free_month = now + datetime.timedelta(days=30)

        cur.execute("INSERT INTO users (email, password, plan, created_at, expired_at) VALUES (?, ?, 'free', ?, ?)", 
                    (email, password, now.isoformat(), free_month.isoformat()))

        conn.commit()
        conn.close()
        return jsonify({"status":"ok","message":"تم إنشاء الحساب بنجاح"})
    except:
        return jsonify({"status":"error","message":"هذا البريد مستخدم من قبل"})
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # سر للجت توكن – غيّرو في الحقيقة
    app.config["SECRET_KEY"] = "CHANGE_THIS_TO_A_STRONG_SECRET"
    app.config["JWT_SECRET_KEY"] = "CHANGE_THIS_JWT_SECRET_TOO"

    # تفعيل CORS للفرونت
    CORS(app)

    # تهيئة الإضافات
    bcrypt.init_app(app)
    jwt.init_app(app)

    # إنشاء الجداول
    init_db()

    # تسجيل البلوبرنتس
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(payments_bp, url_prefix="/payments")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
