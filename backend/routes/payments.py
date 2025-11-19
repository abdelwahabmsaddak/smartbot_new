from flask import Blueprint, request, jsonify
import requests
from config import Config

payments_bp = Blueprint("payments", __name__)

# Create PayPal Order
@payments_bp.post("/create-order")
def create_order():
    data = request.json
    amount = data.get("amount", "29.00")

    auth = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        auth=(Config.PAYPAL_CLIENT_ID, Config.PAYPAL_SECRET),
        data={"grant_type": "client_credentials"}
    ).json()

    access_token = auth["access_token"]

    order = requests.post(
        "https://api-m.sandbox.paypal.com/v2/checkout/orders",
        headers={"Authorization": f"Bearer {access_token}",
                 "Content-Type": "application/json"},
        json={
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {"currency_code": "USD", "value": amount}
            }]
        }
    ).json()

    return jsonify(order)
