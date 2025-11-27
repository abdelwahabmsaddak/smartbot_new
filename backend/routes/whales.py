from flask import Blueprint, jsonify
import requests
import random
from backend.ai_trader import smart_ai  # الذكاء الاصطناعي الموحد

whales_bp = Blueprint("whales", __name__)

# API وهمي – يمكنك تغيير الرابط لأي منصة Whale Alert حقيقية
WHALE_API = "https://api.whale-alert.io/v1/transactions?api_key=demo"


@whales_bp.get("/api/whales")
def whales():
    """جلب تحويلات الحيتان"""
    # بيانات وهمية – حتى يعمل الموقع دون API حقيقية
    sample = [
        {
            "amount": round(random.uniform(1000000, 8000000), 2),
            "from": "Unknown Wallet",
            "to": "Binance",
            "time": "Just Now"
        },
        {
            "amount": round(random.uniform(500000, 2000000), 2),
            "from": "Coinbase",
            "to": "Private Wallet",
            "time": "2 min ago"
        }
    ]
    return jsonify(sample)


@whales_bp.get("/api/whales/ai_analyze")
def whales_ai_analyze():
    """تحليل ذكي باستعمال نفس AI المستخدم في كل الصفحات"""
    text = """
    هذه بيانات تحويلات الحيتان. استخرج الاتجاهات المحتملة
    - هل السوق صاعد أم هابط؟
    - هل هناك تراكم أم توزيع؟
    - تأثير ذلك على البيتكوين والعملات البديلة؟
    """

    result = smart_ai(text)  # نموذج الذكاء الاصطناعي الموحد
    return result
