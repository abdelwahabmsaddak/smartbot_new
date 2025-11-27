# backend/routes/screener.py

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
import yfinance as yf
import talib
import numpy as np

screener_bp = Blueprint("screener", __name__)

@bp.route("/screener_ai")
def screener_ai():
    coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    results = {c: SmartAI.analyze(c) for c in coins}
    return jsonify(results)
    
# قوائم جاهزة (تنجم تبدّلهم من بعد من الـ DB)
WATCHLIST = {
    "crypto": [
        "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD",
        "PEPE-USD", "FLOKI-USD"
    ],
    "stocks": [
        "AAPL", "MSFT", "TSLA", "AMZN", "NVDA"
    ],
    "gold": [
        "XAUUSD=X",  # ذهب
        "GC=F"       # عقد ذهب في ياهو فايننس
    ]
}


@screener_bp.route("/screener")
def screener_page():
    """صفحة الواجهة (templates/market_screener.html مثلاً)"""
    return render_template("market_screener.html")


@screener_bp.route("/api/screener", methods=["POST"])
def screener_api():
    """
    API رئيسي للسكرينر الاحترافي:
    - يأخذ: market, indicators, min_volume, timeframe, lookback, sort_by
    - يرجّع: قائمة رموز مع مؤشرات وتحليل بسيط.
    """
    data = request.get_json() or {}

    market = data.get("market", "crypto")          # crypto | stocks | gold
    indicators = data.get("indicators", [])        # مثال: ["rsi", "ema", "bb"]
    min_volume = float(data.get("min_volume", 0))
    timeframe = data.get("timeframe", "1d")        # 1d, 4h, 1h ...
    lookback = int(data.get("lookback", 120))      # عدد الشمعات
    sort_by = data.get("sort_by", "volume")        # volume | rsi | smart_score

    symbols = WATCHLIST.get(market, WATCHLIST["crypto"])
    end = datetime.utcnow()
    start = end - timedelta(days=lookback * 3)

    results = []

    for symbol in symbols:
        try:
            df = yf.download(
                symbol,
                start=start,
                end=end,
                interval=timeframe,
                progress=False
            )

            if df.empty:
                continue

            df = df.dropna()
            close = df["Close"]
            volume = df["Volume"]

            last_price = float(close.iloc[-1])
            last_volume = float(volume.iloc[-1])

            if last_volume < min_volume:
                # فلترة حسب الحجم
                continue

            row = {
                "symbol": symbol,
                "price": round(last_price, 6),
                "volume": int(last_volume),
            }

            # ===== RSI =====
            if "rsi" in indicators:
                rsi = talib.RSI(close, timeperiod=14)
                row["rsi"] = float(rsi.iloc[-1])

            # ===== EMA 50 / EMA 200 + اتجاه الترند =====
            if "ema" in indicators:
                ema50 = talib.EMA(close, timeperiod=50)
                ema200 = talib.EMA(close, timeperiod=200)
                row["ema50"] = float(ema50.iloc[-1])
                row["ema200"] = float(ema200.iloc[-1])
                row["trend"] = "bullish" if row["ema50"] > row["ema200"] else "bearish"

            # ===== Bollinger Bands =====
            if "bb" in indicators:
                upper, middle, lower = talib.BBANDS(
                    close,
                    timeperiod=20,
                    nbdevup=2,
                    nbdevdn=2,
                    matype=0
                )
                last_close = close.iloc[-1]
                u = upper.iloc[-1]
                l = lower.iloc[-1]

                if last_close > u:
                    bb_pos = " فوق الباند العلوي (تشبّع شراء)"
                elif last_close < l:
                    bb_pos = " تحت الباند السفلي (تشبّع بيع)"
                else:
                    bb_pos = " داخل الباندات"
                row["bb_position"] = bb_pos

            # ===== "Smart Score" بسيط يجمع المؤشرات =====
            score = 0
            # مثال بسيط: نعطي نقاط حسب المؤشرات
            if "rsi" in row:
                if row["rsi"] < 30:
                    score += 2   # منطقة شراء محتملة
                elif row["rsi"] > 70:
                    score -= 2   # منطقة بيع محتملة

            if "trend" in row:
                if row["trend"] == "bullish":
                    score += 1
                else:
                    score -= 1

            if "bb_position" in row:
                if "تحت الباند" in row["bb_position"]:
                    score += 1
                elif "فوق الباند" in row["bb_position"]:
                    score -= 1

            row["smart_score"] = score

            results.append(row)

        except Exception as e:
            # ما نطيحوش السيرفر لو رمز واحد فيه مشكلة
            continue

    # ترتيب النتائج
    reverse = True
    try:
        results = sorted(results, key=lambda x: x.get(sort_by, 0), reverse=reverse)
    except Exception:
        results = sorted(results, key=lambda x: x.get("volume", 0), reverse=True)

    return jsonify({"results": results, "count": len(results)})
