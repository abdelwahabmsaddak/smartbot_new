from flask import Blueprint, request, jsonify
import ccxt
import time

multi_bp = Blueprint("multi_trading", __name__)

# ---------------------------
#  Helper: إنشاء الإكسشانج
# ---------------------------
def create_exchange(platform, api_key, api_secret):
    platform = platform.lower()

    exchanges = {
        "binance": ccxt.binance,
        "kucoin": ccxt.kucoin,
        "bybit": ccxt.bybit,
        "okx": ccxt.okx,
        "coinbase": ccxt.coinbasepro
    }

    if platform not in exchanges:
        raise Exception("❌ منصة غير مدعومة")

    exchange_class = exchanges[platform]

    return exchange_class({
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True
    })


# ---------------------------
# 1️⃣  الحصول على السعر
# ---------------------------
@multi_bp.route("/multi/price", methods=["POST"])
def multi_price():
    data = request.json
    platform = data.get("platform")
    symbol = data.get("symbol")  # مثال BTC/USDT

    ex = create_exchange(platform, "", "")
    ticker = ex.fetch_ticker(symbol)

    return jsonify({
        "symbol": symbol,
        "price": ticker["last"]
    })


# ---------------------------
# 2️⃣  الحصول على الرصيد
# ---------------------------
@multi_bp.route("/multi/balance", methods=["POST"])
def multi_balance():
    data = request.json
    platform = data["platform"]
    api_key = data["api_key"]
    api_secret = data["api_secret"]

    ex = create_exchange(platform, api_key, api_secret)
    balance = ex.fetch_balance()

    return jsonify(balance)


# ---------------------------
# 3️⃣  تنفيذ صفقة (buy/sell)
# ---------------------------
@multi_bp.route("/multi/order", methods=["POST"])
def multi_order():
    data = request.json
    platform = data["platform"]
    api_key = data["api_key"]
    api_secret = data["api_secret"]
    symbol = data["symbol"]
    side = data["side"]          # buy أو sell
    amount = data["amount"]      # الكمية
    price = data.get("price")    # للسوق نقولو None

    ex = create_exchange(platform, api_key, api_secret)

    if price:
        order = ex.create_limit_order(symbol, side, amount, price)
    else:
        order = ex.create_market_order(symbol, side, amount)

    return jsonify(order)


# ---------------------------
# 4️⃣  إلغاء صفقة
# ---------------------------
@multi_bp.route("/multi/cancel", methods=["POST"])
def multi_cancel():
    data = request.json
    platform = data["platform"]
    api_key = data["api_key"]
    api_secret = data["api_secret"]
    symbol = data["symbol"]
    order_id = data["order_id"]

    ex = create_exchange(platform, api_key, api_secret)
    result = ex.cancel_order(order_id, symbol)

    return jsonify(result)
