import requests
from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_db, User
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

router = APIRouter(prefix="/billing", tags=["billing"])

PAYPAL_CLIENT_ID = "YOUR_PAYPAL_CLIENT_ID"
PAYPAL_SECRET = "YOUR_PAYPAL_SECRET"
PAYPAL_API = "https://api-m.paypal.com"   # Production
# PAYPAL_API = "https://api-m.sandbox.paypal.com"  # Sandbox (اختبار)

# ====================================================
# 1) Get PayPal Access Token
# ====================================================

def get_paypal_token():
    response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )
    if response.status_code != 200:
        raise HTTPException(500, "PayPal token error")
    return response.json()["access_token"]

# ====================================================
# 2) Create subscription
# ====================================================

@router.post("/create-subscription")
def create_subscription(user_id: int, db: Session = Depends(get_db)):
    token = get_paypal_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    body = {
        "plan_id": "P-1234567890123456",  # ID متاع الخطة من PayPal
        "subscriber": {
            "email_address": db.query(User).filter(User.id == user_id).first().email
        },
        "application_context": {
            "return_url": "https://YOUR_DOMAIN/success",
            "cancel_url": "https://YOUR_DOMAIN/cancel",
        },
    }

    r = requests.post(
        f"{PAYPAL_API}/v1/billing/subscriptions",
        json=body,
        headers=headers,
    )

    if r.status_code not in [200, 201]:
        print(r.text)
        raise HTTPException(500, "PayPal subscription error")

    return r.json()

# ====================================================
# 3) Webhook (تفعيل الاشتراك بعد الدفع)
# ====================================================

@router.post("/webhook")
def paypal_webhook(payload: dict, db: Session = Depends(get_db)):
    event = payload.get("event_type")

    # اشتراك جديد
    if event == "BILLING.SUBSCRIPTION.ACTIVATED":
        subscription = payload["resource"]
        email = subscription["subscriber"]["email_address"]

        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_active = True
            user.trial_ends_at = None
            db.commit()

    return {"status": "ok"}
