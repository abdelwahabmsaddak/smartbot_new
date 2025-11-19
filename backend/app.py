from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .database import init_db
from .routes.auth import auth_bp
from .routes.api import api_bp
from .routes.payments import payments_bp  # نجهزه كستب لاحقة


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
