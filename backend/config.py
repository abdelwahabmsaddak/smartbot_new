# backend/config.py
import os

# ===== إعدادات قاعدة البيانات ... (اترك اللي عندك) =====

# ===== إعدادات بايبال =====
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "YOUR_PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "YOUR_PAYPAL_SECRET")

# للـ Sandbox:
PAYPAL_BASE_URL = os.getenv(
    "PAYPAL_BASE_URL",
    "https://api-m.sandbox.paypal.com"
)

# لما تمر للإنتاج غيّرها إلى:
# "https://api-m.paypal.com"
