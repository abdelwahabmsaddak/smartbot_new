from flask import Flask
from flask_cors import CORS
import os

# ============================
# IMPORT BLUEPRINTS
# ============================
from backend.routes.auth import auth_bp
from backend.routes.admin import admin_bp
from backend.routes.profile import profile_bp
from backend.routes.chatbot import chatbot_bp
from backend.routes.usage import usage_bp
from backend.routes.payments import payments_bp
from backend.routes.billing import billing_bp
from backend.routes.affiliate import affiliate_bp
from backend.routes.settings import settings_bp
from backend.routes.api_keys import api_keys_bp
from backend.routes.ai_trader import ai_trader_bp
from backend.routes.whales import whales_bp
from backend.routes.screener import screener_bp
from backend.routes.auto_trading import auto_trading_bp
from backend.routes.auto_trading_pro import auto_trading_pro_bp
from backend.routes.withdraw import withdraw_bp
from backend.routes.blog import blog_bp
from backend.routes.notifications import notifications_bp
from backend.routes.multi_trading import multi_trading_bp
from backend.routes.analysis import analysis_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.secret_key = os.getenv("SECRET_KEY", "SMARTBOT_SUPER_SECRET")

    # ============================
    # REGISTER BLUEPRINTS
    # ============================
    blueprints = [
        auth_bp,
        admin_bp,
        profile_bp,
        chatbot_bp,
        usage_bp,
        payments_bp,
        billing_bp,
        affiliate_bp,
        settings_bp,
        api_keys_bp,
        ai_trader_bp,
        whales_bp,
        screener_bp,
        auto_trading_bp,
        auto_trading_pro_bp,
        withdraw_bp,
        blog_bp,
        notifications_bp,
        multi_trading_bp,
        analysis_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route("/")
    def home():
        return "SmartBot Backend Running Successfully"

    return app


# ============================
# RUN APP (Render)
# ============================
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
