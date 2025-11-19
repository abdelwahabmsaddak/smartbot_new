from fastapi import APIRouter, HTTPException, Request, Depends
import httpx
import os
from backend.database import get_db, User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/payments", tags=["payments"])

PAYPAL_CLIENT_ID = "AarCp3bOi8dxdhk46lTloPQNQlte2Pmmkbu1LpLQ71NB1ySsabbNzPTptrAmEldzTS2fLgc7QIQF9Ja5"
PAYPAL_SECRET = "EEwlQPjsT_ti3WeXNzmOyfJZOEFqpUkj86dMH6Tc5aWN1t6Wv3Z8befhiSC33UuUe9MlvYo8ygaBYKFe"

BASE_URL = "https://api-m.sandbox.paypal.com"

# ================================
# 1) إنشاء اشتراك جديد
# ================================
@router.post("/create-subscription")
async def create_subscription():
    async with httpx.AsyncClient() as client:
        # Token
        auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
        data = {"grant_type": "client_credentials"}

        r = await client.post(f"{BASE_URL}/v1/oauth2/token", data=data, auth=auth)
        access_token = r.json()["access_token"]

        # Create subscription
        headers = {"Authorization": f"Bearer {access_token}"}
        body = {
            "plan_id": "P-12345678912345678",  # 👈 ستعطيهولك بعد نعمل Plan رسمي
            "application_context": {
                "return_url": "https://smartbot-new.onrender.com/subscription",
                "cancel_url": "https://smartbot-new.onrender.com/subscription"
            }
        }

        r = await client.post(f"{BASE_URL}/v1/billing/subscriptions", json=body, headers=headers)
        return r.json()

# ================================
# 2) Webhook — PayPal → موقعك
# ================================
@router.post("/webhook")
async def webhook_listener(request: Request, db: Session = Depends(get_db)):
    event = await request.json()

    event_type = event.get("event_type")
    resource = event.get("resource", {})

    subscription_id = resource.get("id")
    status = resource.get("status")

    # مثال: تحديث حالة المستخدم
    if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
        user = db.query(User).filter(User.subscription_id == subscription_id).first()
        if user:
            user.is_active = True
            db.commit()

    elif event_type == "BILLING.SUBSCRIPTION.CANCELLED":
        user = db.query(User).filter(User.subscription_id == subscription_id).first()
        if user:
            user.is_active = False
            db.commit()

    return {"status": "ok"}
