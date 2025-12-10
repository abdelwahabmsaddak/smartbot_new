from flask import Flask, render_template
from backend.routes.admin import admin_bp
from backend.routes.profile import profile_bp
from backend.routes.auth import auth_bp
from backend.routes.usage import usage_bp
from backend.routes.chatbot import chatbot_bp
from backend.routes.payments import payments_bp
from backend.routes.billing import billing_bp
from backend.routes.affiliate import affiliate_bp
from backend.routes.settings import settings_bp
from backend.routes.api_keys import api_keys_bp
from backend.routes.ai_trader import ai_trader_bp
from backend.routes.whales import whales_bp
from backend.routes.screener import screener_bp
from backend.routes.auto_trading import auto_bp

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(auth_bp)
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


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
