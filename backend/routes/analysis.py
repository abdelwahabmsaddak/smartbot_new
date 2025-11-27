from flask import Blueprint, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

analysis_bp = Blueprint("analysis_bp", __name__)

from ai_core import SmartAI

@bp.route("/analysis_ai", methods=["POST"])
def analysis_ai():
    data = request.json
    symbol = data["symbol"]
    tf = data.get("tf", "1h")

    result = SmartAI.analyze(symbol, tf)
    return jsonify({"ai_analysis": result})
    
# ---------- Helpers ----------

def normalize_symbol(symbol: str) -> str:
    """
    نحاول نخلي الرمز يخدم للكريبتو + الأسهم + الذهب
    - BTCUSDT  -> BTC-USD (ياهو فاينانس)
    - ethusdt  -> ETH-USD
    - الباقي نخليه كما هو (AAPL, TSLA, GC=F, XAUUSD=X, ...)
    """
    if not symbol:
        return ""
    s = symbol.upper().strip()
    if s.endswith("USDT"):
        base = s[:-4]
        return f"{base}-USD"
    return s


def get_history(symbol: str, period="90d", interval="1h"):
    """
    جلب البيانات التاريخية من yfinance
    تخدم للكريبتو، الأسهم، و الذهب (حسب الرمز).
    """
    norm = normalize_symbol(symbol)
    data = yf.download(norm, period=period, interval=interval, progress=False)
    if data is None or data.empty:
        raise ValueError(f"ما لقيتش بيانات للرمز: {symbol}")
    return data


# ---------------- Indicators ----------------

def calc_ma(close, window=50):
    return close.rolling(window=window).mean()

def calc_ema(close, window=50):
    return close.ewm(span=window, adjust=False).mean()

def calc_rsi(close, period=14):
    delta = close.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    gain_ema = pd.Series(gain).ewm(span=period, adjust=False).mean()
    loss_ema = pd.Series(loss).ewm(span=period, adjust=False).mean()
    rs = gain_ema / (loss_ema + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calc_macd(close, fast=12, slow=26, signal=9):
    ema_fast = calc_ema(close, fast)
    ema_slow = calc_ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def calc_bollinger(close, window=20, num_std=2):
    ma = calc_ma(close, window)
    std = close.rolling(window=window).std()
    upper = ma + num_std * std
    lower = ma - num_std * std
    return ma, upper, lower

def calc_stoch(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = (close - lowest_low) * 100 / (highest_high - lowest_low + 1e-9)
    d = k.rolling(window=d_period).mean()
    return k, d

def volume_trend(volume):
    """
    مؤشر بسيط: نقارن متوسط آخر 5 شمعات بمتوسط آخر 20 شمعة
    """
    short = volume.rolling(window=5).mean()
    long = volume.rolling(window=20).mean()
    return short, long

def support_resistance(close, window=30):
    """
    دعم ومقاومة تقريبية: أدنى و أعلى سعر في آخر N شمعة.
    """
    recent = close.tail(window)
    support = recent.min()
    resistance = recent.max()
    return support, resistance

def whales_activity(volume, window=30):
    """
    'تتبع الحيتان' بشكل تقريبي: إذا كان في سبايك كبير في الحجم.
    نعتبر حيتان إذا آخر حجم > متوسط 30 * 2
    """
    recent = volume.tail(window)
    avg = recent.mean()
    last = recent.iloc[-1]
    ratio = last / (avg + 1e-9)
    return last, avg, ratio

# ---------------- Smart Analysis ----------------

def build_smart_analysis(close, indicators_result):
    """
    نعمل Score موحد من -100 (بيع قوي) إلى +100 (شراء قوي)
    نعطي لكل مؤشر صوت حسب إشارته.
    """
    score = 0
    votes = 0
    comments = []

    def vote(direction, weight, reason):
        nonlocal score, votes, comments
        if direction == "bullish":
            score += weight
        elif direction == "bearish":
            score -= weight
        votes += weight
        comments.append(reason)

    last_price = float(close.iloc[-1])

    # MA
    ma_info = indicators_result.get("ma")
    if ma_info:
        vote(ma_info["direction"], 2, "إشارة المتوسط المتحرك: " + ma_info["signal"])

    # EMA
    ema_info = indicators_result.get("ema")
    if ema_info:
        vote(ema_info["direction"], 2, "إشارة EMA: " + ema_info["signal"])

    # RSI
    rsi_info = indicators_result.get("rsi")
    if rsi_info:
        vote(rsi_info["direction"], 2, "RSI: " + rsi_info["signal"])

    # MACD
    macd_info = indicators_result.get("macd")
    if macd_info:
        vote(macd_info["direction"], 2, "MACD: " + macd_info["signal"])

    # Bollinger
    bb_info = indicators_result.get("bb")
    if bb_info:
        vote(bb_info["direction"], 1.5, "بولينجر: " + bb_info["signal"])

    # Stoch
    stoch_info = indicators_result.get("stoch")
    if stoch_info:
        vote(stoch_info["direction"], 1.5, "ستوكاستيك: " + stoch_info["signal"])

    # Volume / Whales
    vol_info = indicators_result.get("volume")
    if vol_info:
        vote(vol_info["direction"], 1, "الحجم: " + vol_info["signal"])

    whales_info = indicators_result.get("whales")
    if whales_info:
        vote(whales_info["direction"], 1, "الحيتان: " + whales_info["signal"])

    # Support/Resistance
    sr_info = indicators_result.get("support")
    if sr_info:
        vote(sr_info["direction"], 1, "الدعم/المقاومة: " + sr_info["signal"])

    if votes == 0:
        smart_score = 0
    else:
        smart_score = round((score / (votes * 1.0)) * 100, 2)

    if smart_score > 40:
        final_signal = "شراء (Bullish)"
    elif smart_score < -40:
        final_signal = "بيع (Bearish)"
    else:
        final_signal = "حيادي"

    return {
        "price": round(last_price, 6),
        "smart_score": smart_score,
        "final_signal": final_signal,
        "short_comment": " - ".join(comments[-4:])  # آخر ٤ تعاليق فقط
    }


# ---------------- Routes ----------------

@analysis_bp.route("/analysis")
def analysis_page():
    # صفحة HTML اللي وريتهالي (advanced analysis)
    return render_template("analysis.html")


@analysis_bp.route("/analysis_api", methods=["POST"])
def analysis_api():
    data = request.get_json() or {}
    symbol = data.get("symbol", "").strip()
    requested_indicators = data.get("indicators", [])

    if not symbol:
        return jsonify({"error": "الرمز مطلوب"}), 400

    try:
        df = get_history(symbol)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    results = {}

    # === MA ===
    if "ma" in requested_indicators:
        ma50 = calc_ma(close, 50).iloc[-1]
        ma200 = calc_ma(close, 200).iloc[-1]
        last = close.iloc[-1]
        if last > ma50 and ma50 > ma200:
            direction = "bullish"
            signal = "السعر فوق MA50 و MA200 (اتجاه صاعد)"
        elif last < ma50 and ma50 < ma200:
            direction = "bearish"
            signal = "السعر تحت MA50 و MA200 (اتجاه هابط)"
        else:
            direction = "neutral"
            signal = "السعر قريب من المتوسطات (اتجاه جانبي)"
        results["ma"] = {
            "value_50": round(float(ma50), 6),
            "value_200": round(float(ma200), 6),
            "direction": direction,
            "signal": signal,
        }

    # === EMA (مؤشر جديد) ===
    if "ema" in requested_indicators:
        ema21 = calc_ema(close, 21).iloc[-1]
        ema55 = calc_ema(close, 55).iloc[-1]
        last = close.iloc[-1]
        if last > ema21 > ema55:
            direction = "bullish"
            signal = "EMA21 فوق EMA55 والسعر فوقهم (زخم صاعد قوي)"
        elif last < ema21 < ema55:
            direction = "bearish"
            signal = "EMA21 تحت EMA55 والسعر تحتهم (زخم هابط قوي)"
        else:
            direction = "neutral"
            signal = "EMA متقاربة (سوق متذبذب)"
        results["ema"] = {
            "value_21": round(float(ema21), 6),
            "value_55": round(float(ema55), 6),
            "direction": direction,
            "signal": signal,
        }

    # === RSI ===
    if "rsi" in requested_indicators:
        rsi_series = calc_rsi(close)
        rsi = float(rsi_series.iloc[-1])
        if rsi > 70:
            direction = "bearish"
            signal = "RSI في منطقة تشبع شرائي (احتمال تصحيح)"
        elif rsi < 30:
            direction = "bullish"
            signal = "RSI في منطقة تشبع بيعي (احتمال ارتداد)"
        else:
            direction = "neutral"
            signal = "RSI في منطقة متوازنة"
        results["rsi"] = {
            "value": round(rsi, 2),
            "direction": direction,
            "signal": signal,
        }

    # === MACD ===
    if "macd" in requested_indicators:
        macd_line, signal_line, hist = calc_macd(close)
        last_macd = float(macd_line.iloc[-1])
        last_signal = float(signal_line.iloc[-1])
        last_hist = float(hist.iloc[-1])
        if last_macd > last_signal and last_hist > 0:
            direction = "bullish"
            signal = "تقاطع MACD لأعلى (زخم صاعد)"
        elif last_macd < last_signal and last_hist < 0:
            direction = "bearish"
            signal = "تقاطع MACD لأسفل (زخم هابط)"
        else:
            direction = "neutral"
            signal = "MACD بدون إشارة قوية"
        results["macd"] = {
            "macd": round(last_macd, 4),
            "signal_line": round(last_signal, 4),
            "hist": round(last_hist, 4),
            "direction": direction,
            "signal": signal,
        }

    # === Bollinger Bands (مؤشر جديد) ===
    if "bb" in requested_indicators:
        mid, upper, lower = calc_bollinger(close)
        last_mid = float(mid.iloc[-1])
        last_upper = float(upper.iloc[-1])
        last_lower = float(lower.iloc[-1])
        last_price = float(close.iloc[-1])

        if last_price > last_upper:
            direction = "bearish"
            signal = "السعر فوق الحد العلوي لبولينجر (ممكن تصحيح)"
        elif last_price < last_lower:
            direction = "bullish"
            signal = "السعر تحت الحد السفلي لبولينجر (ممكن ارتداد)"
        else:
            direction = "neutral"
            signal = "السعر داخل قناة بولينجر (حركة طبيعية)"
        results["bb"] = {
            "middle": round(last_mid, 6),
            "upper": round(last_upper, 6),
            "lower": round(last_lower, 6),
            "direction": direction,
            "signal": signal,
        }

    # === Stochastic ===
    if "stoch" in requested_indicators:
        k, d = calc_stoch(high, low, close)
        last_k = float(k.iloc[-1])
        last_d = float(d.iloc[-1])
        if last_k > 80 and last_d > 80:
            direction = "bearish"
            signal = "Stoch في تشبع شرائي"
        elif last_k < 20 and last_d < 20:
            direction = "bullish"
            signal = "Stoch في تشبع بيعي"
        else:
            direction = "neutral"
            signal = "Stoch طبيعي"
        results["stoch"] = {
            "k": round(last_k, 2),
            "d": round(last_d, 2),
            "direction": direction,
            "signal": signal,
        }

    # === Volume Trend ===
    if "volume" in requested_indicators:
        short, long = volume_trend(volume)
        last_short = float(short.iloc[-1])
        last_long = float(long.iloc[-1])
        if last_short > last_long * 1.5:
            direction = "bullish"
            signal = "حجم تداول أعلى من المتوسط (اهتمام قوي)"
        elif last_short < last_long * 0.7:
            direction = "bearish"
            signal = "حجم تداول ضعيف (اهتمام ضعيف)"
        else:
            direction = "neutral"
            signal = "حجم تداول عادي"
        results["volume"] = {
            "short_ma": round(last_short, 2),
            "long_ma": round(last_long, 2),
            "direction": direction,
            "signal": signal,
        }

    # === Support / Resistance ===
    if "support" in requested_indicators:
        support, resistance = support_resistance(close)
        last_price = float(close.iloc[-1])
        if last_price <= support * 1.02:
            direction = "bullish"
            signal = "السعر قريب من منطقة دعم (ممكن ارتداد)"
        elif last_price >= resistance * 0.98:
            direction = "bearish"
            signal = "السعر قريب من مقاومة (ممكن تصحيح)"
        else:
            direction = "neutral"
            signal = "السعر بين الدعم والمقاومة"
        results["support"] = {
            "support": round(float(support), 6),
            "resistance": round(float(resistance), 6),
            "direction": direction,
            "signal": signal,
        }

    # === Whales (Volume Spikes) ===
    if "whales" in requested_indicators:
        last_vol, avg_vol, ratio = whales_activity(volume)
        if ratio > 2:
            direction = "bullish"
            signal = "سبايك حجم كبير (دخول حيتان/محافظ كبيرة)"
        elif ratio < 0.5:
            direction = "bearish"
            signal = "حجم أقل بكثير من العادة"
        else:
            direction = "neutral"
            signal = "حجم قريب من المتوسط"
        results["whales"] = {
            "last_volume": round(float(last_vol), 2),
            "avg_volume": round(float(avg_vol), 2),
            "ratio": round(float(ratio), 2),
            "direction": direction,
            "signal": signal,
        }

    # ---------- Smart unified analysis ----------
    smart = build_smart_analysis(close, results)

    response = {
        "symbol": symbol.upper(),
        "normalized_symbol": normalize_symbol(symbol),
        "smart_analysis": smart,
        "indicators": results,
    }
    return jsonify(response)
