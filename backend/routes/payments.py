import requests
from fastapi import APIRouter, HTTPException
from backend.config import PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY, PAYPAL_API_BASE

router = APIRouter(prefix="/payments", tags=["payments"])

# 1) إنشاء توكن اتصال مع PayPal
def generate_access_token():
    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY),
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="PayPal Auth Failed")
    
    return response.json()["access_token"]


# 2) إنشاء عملية دفع
@router.post("/create")
def create_payment():
    token = generate_access_token()

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "29.00"
                }
            }
        ],
        "application_context": {
            "return_url": "https://smartbot.com/thankyou",
            "cancel_url": "https://smartbot.com/cancel"
        }
    }

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders",
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="PayPal Payment Failed")

    return response.json()


# 3) تأكيد الدفع بعد رجوع العميل من PayPal
@router.get("/capture/{order_id}")
def capture_payment(order_id: str):
    token = generate_access_token()

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Payment Capture Failed")

    return response.json()
