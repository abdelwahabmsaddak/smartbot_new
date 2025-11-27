from flask import Blueprint, request, jsonify
import yfinance as yf
import talib
import numpy as np

ai_trader_bp = Blueprint("ai_trader", __name__)

def analyze_symbol(symbol):
    data = yf.download(symbol, period="3mo", interval="1d")
    if data.empty:
        return "❌ رمز غير صحيح"

    close = data["Close"]

    # Indicators
    rsi = talib.RSI(close, timeperiod=14)[-1]
    ma = talib.SMA(close, timeperiod=20)[-1]

    trend = "📈 صاعد" if close.iloc[-1] > ma else "📉 هابط"

    # Simple AI logic
    if rsi < 30:
        ai = "العملة في منطقة شراء قوية (Oversold)"
    elif rsi > 70:
        ai = "تحذير: منطقة بيع (Overbought)"
    else:
        ai = "الاتجاه طبيعي حالياً."

    return f"""
🔍 تحليل: {symbol}
💹 الاتجاه: {trend}
📊 RSI: {round(rsi, 2)}
📏 MA20: {round(ma, 2)}

🤖 الذكاء الاصطناعي:
{ai}

🎯 الرأي النهائي:
{ 'ينصح بالشراء' if rsi < 30 else 'ينصح بالانتظار' }
"""

@ai_trader_bp.post("/api/ai_trader")
def ai_trader_api():
    msg = request.json.get("message", "")

    # Detect symbol from message
    words = msg.upper().split()
    symbol = None
    for w in words:
        if len(w) >= 3:
            symbol = w
            break

    if symbol:
        reply = analyze_symbol(symbol)
    else:
        reply = "اكتب اسم عملة أو سهم مثل: BTC-USD أو AAPL"

    return jsonify({"reply": reply})
