from datetime import datetime
import requests

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import SessionLocal, User
from backend import config


router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


# ====== موديلات للـ API ======

class PlanInfo(BaseModel):
    name: str
    price: float
    currency: str
    trial_days: int
    description: str


class PaypalSubscriptionRequest(BaseModel):
    user_id: int  # مؤقتاً يجي من الفرونت (ID المستخدم بعد تسجيل الدخول)


class PaypalSubscriptionResponse(BaseModel):
    approve_url: str


# ====== معلومات الباقة (شهر مجاني + 29$) ======

@router.get("/plan", response_model=PlanInfo)
def get_plan_info():
    """
    ترجع معلومات الباقة لعرضها في الواجهة:
    - شهر أول مجاني
    - بعده 29$ شهرياً يشمل كل المميزات
    """
    return PlanInfo(
        name=config.PLAN_NAME,
        price=config.PLAN_PRICE,
        currency=config.PLAN_CURRENCY,
        trial_days=config.PLAN_TRIAL_DAYS,
        description=(
            "شهر أول مجاني، بعده 29$ / شهر يشمل كل المميزات: "
            "تحليل العملات، الذهب، الأسهم، التداول الآلي، التنبيهات، تتبع الحيتان، "
            "المدونة، والدردشة."
        ),
    )


# ====== دوال مساعدة للـ PayPal ======

def _get_paypal_access_token() -> str:
    """
    تأخذ access token من PayPal باستخدام client_id / client_secret
    """
    if not config.PAYPAL_CLIENT_ID or not config.PAYPAL_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="إعدادات PayPal غير مكتملة (CLIENT_ID / CLIENT_SECRET غير موجودة).",
        )

    resp = requests.post(
        f"{config.PAYPAL_BASE_URL}/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        auth=(config.PAYPAL_CLIENT_ID, config.PAYPAL_CLIENT_SECRET),
    )

    if resp.status_code != 200:
        print("PayPal token error:", resp.text)
        raise HTTPException(status_code=500, detail="فشل الحصول على توكن من PayPal")

    data = resp.json()
    return data["access_token"]


# ====== إنشاء اشتراك PayPal شهري ======

@router.post(
    "/paypal/create-subscription",
    response_model=PaypalSubscriptionResponse,
)
def create_paypal_subscription(body: PaypalSubscriptionRequest):
    """
    تنشئ اشتراك شهري عبر PayPal لخطة واحدة:
    - شهر مجاني من داخل الموقع (trial_end)
    - بعد الموافقة في PayPal يبدأ خصم 29$ شهرياً حسب الخطة في PayPal.
    """
    if not config.PAYPAL_PLAN_ID:
        raise HTTPException(
            status_code=500,
            detail="PAYPAL_PLAN_ID غير مضبوط في الإعدادات.",
        )

    db = SessionLocal()

    try:
        # تأكد أن المستخدم موجود
        user = db.query(User).filter(User.id == body.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="المستخدم غير موجود")

        access_token = _get_paypal_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "plan_id": config.PAYPAL_PLAN_ID,
            "subscriber": {
                "email_address": user.email,
            },
            "application_context": {
                "brand_name": "SmartBot",
                "locale": "ar-EG",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "SUBSCRIBE_NOW",
                "return_url": "https://smartbot-ai-1.onrender.com/success",
                "cancel_url": "https://smartbot-ai-1.onrender.com/cancel",
            },
        }

        resp = requests.post(
            f"{config.PAYPAL_BASE_URL}/v1/billing/subscriptions",
            json=payload,
            headers=headers,
        )

        if resp.status_code not in (200, 201):
            print("PayPal subscription error:", resp.text)
            raise HTTPException(
                status_code=500,
                detail="فشل إنشاء الاشتراك في PayPal",
            )

        sub_data = resp.json()

        # رابط الموافقة (approve_url)
        approve_url = None
        for link in sub_data.get("links", []):
            if link.get("rel") == "approve":
                approve_url = link.get("href")
                break

        if not approve_url:
            raise HTTPException(
                status_code=500,
                detail="لم يتم العثور على رابط الموافقة من PayPal",
            )

        # حفظ معلومات الاشتراك في قاعدة البيانات
        user.paypal_subscription_id = sub_data["id"]
        user.subscription_status = "pending"
        db.commit()

        return PaypalSubscriptionResponse(approve_url=approve_url)

    finally:
        db.close()
