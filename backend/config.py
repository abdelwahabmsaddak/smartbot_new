import os
from datetime import timedelta
class Config:
    SECRET_KEY = "smartbot_super_secret"
    DATABASE_URL = "sqlite:///smartbot.db"

    PAYPAL_CLIENT_ID = "YOUR_PAYPAL_ID"
    PAYPAL_SECRET = "YOUR_PAYPAL_SECRET"
# =========================
# إعداد باقة الاشتراك
# =========================

PLAN_NAME = "الخطة الكاملة"
PLAN_PRICE = 29          # 29 دولار
PLAN_CURRENCY = "USD"
PLAN_TRIAL_DAYS = 30     # شهر مجاني (30 يوم)

# إعدادات PayPal (ستضع القيم من لوحة PayPal أو من متغيرات البيئة في Render)
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"  # Sandbox للتجارب
PAYPAL_PLAN_ID = os.getenv("PAYPAL_PLAN_ID", "")      # ID الخطة من PayPal Subscriptions
