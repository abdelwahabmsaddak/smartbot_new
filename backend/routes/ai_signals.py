from flask import Blueprint, request, jsonify
import yfinance as yf
import numpy as np

ai_signals_bp = Blueprint("ai_signals", __name__)

# =========================
# 🔥 ذكاء اصطناعي بسيط يعطي:
# BUY / SELL / HOLD
# + درجة ثقة smart_score
# =========================

def calculate_ai_signal(df):
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["RSI"] = compute_rsi(df["Close"])

    last = df.iloc[-1]

    score = 0

    # MA Crossover
    if last["MA20"] > last["MA50"]:
        score += 40
    else:
        score -= 40

    # RSI
    if last["RSI"] < 30:
        score += 40
    elif last["RSI"] > 70:
        score -= 40

    # Trend using last 10 candles
    trend = df["Close"].iloc[-10:].pct_change().sum()
    if trend > 0:
        score += 30
    else:
        score -= 30

    # Normalize to 0–100
    smart_score = int(np.interp(score, [-100, 100], [0, 100]))

    if smart_score >= 66:
        final_signal = "BUY"
    elif smart_score <= 33:
        final_signal = "SELL"
    else:
        final_signal = "HOLD"

    return final_signal, smart_score, float(last["RSI"])


# =========================
# 📌 RSI Function
# =========================
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# =========================
# 📌 API ENDPOINT
# =========================

@ai_signals_bp.route("/api/ai_signal", methods=["POST"])
def ai_signal_api():
    data = request.json
    symbol = data.get("symbol")

    try:
        df = yf.download(symbol, period="3mo", interval="1d")

        if df.empty:
            return jsonify({"error": "رمز غير صالح"}), 400

        df = df.dropna()
        signal, score, rsi = calculate_ai_signal(df)

        return jsonify({
            "symbol": symbol,
            "signal": signal,
            "smart_score": score,
            "rsi": round(rsi, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
