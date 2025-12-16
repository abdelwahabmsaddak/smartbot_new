# backend/routes/pages.py
from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

pages_bp = Blueprint("pages", __name__)

# الصفحة الرئيسية
@pages_bp.route("/")
def home():
    return render_template("index.html")

# صفحات ثابتة بالاسم (باش ما نكتبوش 50 route)
ALLOWED_PAGES = {
    "about", "pricing", "terms", "contact",
    "login", "register",
    "dashboard", "profile", "settings",
    "notifications", "usage", "subscription",
    "users",
    "blog", "edit_post",
    "admin_blog", "admin_dashboard",
    "affiliate", "affiliate_stats",
    "ai_signals", "analysis", "api_keys",
    "autotrade", "auto_trading_pro",
    "chat_widget", "chatbot_trader",
    "market_screener",
    "whales", "whales_alerts",
    "withdraw",
}

@pages_bp.route("/<page>")
def page(page):
    if page not in ALLOWED_PAGES:
        return "Not Found", 404
    try:
        return render_template(f"{page}.html")
    except TemplateNotFound:
        return "Template Not Found", 404
