import re
from typing import Dict, Optional

# =========================
# ASSET MAPS
# =========================

CRYPTO_MAP = {
    "BTC": ["btc", "bitcoin", "بيتكوين", "بتكوين"],
    "ETH": ["eth", "ethereum", "ايثيريوم", "إيثيريوم"],
    "BNB": ["bnb", "binance", "بينانس"],
    "SOL": ["sol", "solana", "سولانا"],
    "XRP": ["xrp", "ripple", "ريبل"],
    "ADA": ["ada", "cardano", "كاردانو"],
    "DOGE": ["doge", "dogecoin", "دوج"],
}

STOCK_MAP = {
    "AAPL": ["aapl", "apple", "آبل"],
    "MSFT": ["msft", "microsoft", "مايكروسوفت"],
    "TSLA": ["tsla", "tesla", "تسلا"],
    "NVDA": ["nvda", "nvidia", "انفيديا"],
    "AMZN": ["amzn", "amazon", "أمازون"],
    "GOOGL": ["googl", "google", "جوجل"],
}

GOLD_KEYWORDS = [
    "gold", "xau", "xauusd",
    "ذهب", "الذهب", "دهب"
]

# =========================
# TIMEFRAMES
# =========================

TIMEFRAME_MAP = {
    "1M": ["1m", "1 دقيقة"],
    "5M": ["5m", "5 دقائق"],
    "15M": ["15m", "15 دقيقة", "ربع ساعة"],
    "30M": ["30m", "30 دقيقة", "نصف ساعة"],
    "1H": ["1h", "ساعة", "1 ساعة"],
    "4H": ["4h", "4 ساعات"],
    "1D": ["1d", "يومي", "يوم"],
    "1W": ["1w", "اسبوع", "أسبوع"],
}

# =========================
# HELPERS
# =========================

def detect_timeframe(text: str) -> Optional[str]:
    for tf, keys in TIMEFRAME_MAP.items():
        for k in keys:
            if k in text:
                return tf
    return None


def normalize_question(text: str) -> str:
    return text.lower().strip()


# =========================
# MAIN DETECTION
# =========================

def detect_asset(question: str) -> Dict:
    """
    Final professional asset detection
    Supports:
    - Arabic / English
    - Crypto / Gold / Stocks
    - Symbols & names
    - Timeframes
    """

    q = normalize_question(question)
    timeframe = detect_timeframe(q)

    # -------- GOLD --------
    for g in GOLD_KEYWORDS:
        if g in q:
            return {
                "type": "gold",
                "symbol": "XAUUSD",
                "name": "Gold",
                "timeframe": timeframe or "1D",
                "confidence": 1.0
            }

    # -------- CRYPTO --------
    for symbol, aliases in CRYPTO_MAP.items():
        for a in aliases:
            if a in q:
                return {
                    "type": "crypto",
                    "symbol": symbol,
                    "name": symbol,
                    "timeframe": timeframe or "4H",
                    "confidence": 1.0
                }

    # -------- KNOWN STOCKS --------
    for symbol, aliases in STOCK_MAP.items():
        for a in aliases:
            if a in q:
                return {
                    "type": "stock",
                    "symbol": symbol,
                    "name": symbol,
                    "timeframe": timeframe or "1D",
                    "confidence": 1.0
                }

    # -------- GENERIC STOCK SYMBOL --------
    match = re.findall(r"\b[A-Z]{2,5}\b", question)
    if match:
        return {
            "type": "stock",
            "symbol": match[0],
            "name": match[0],
            "timeframe": timeframe or "1D",
            "confidence": 0.7
        }

    # -------- FALLBACK --------
    return {
        "type": "unknown",
        "symbol": None,
        "name": None,
        "timeframe": timeframe,
        "confidence": 0.0
    }

import random

def analyze_asset(asset_info: dict) -> dict:
    """
    Smart analysis engine (no external API)
    Returns:
    - trend
    - signal
    - confidence
    - risk
    - whale_hint
    """

    if asset_info["type"] == "unknown":
        return {
            "error": "Unknown asset"
        }

    # -------------------------
    # Simulated market logic
    # (later replace with real indicators)
    # -------------------------

    trend = random.choice(["Bullish", "Bearish", "Neutral"])

    if trend == "Bullish":
        signal = "Buy"
        confidence = random.randint(60, 75)
        risk = "Pullback risk if momentum weakens"
        whale_hint = "Possible accumulation detected"
    elif trend == "Bearish":
        signal = "Sell"
        confidence = random.randint(60, 75)
        risk = "Sharp volatility spikes possible"
        whale_hint = "Exchange inflows suggest distribution"
    else:
        signal = "Wait"
        confidence = random.randint(45, 60)
        risk = "Sideways market, false signals likely"
        whale_hint = "No strong whale activity"

    return {
        "asset": asset_info["symbol"],
        "type": asset_info["type"],
        "timeframe": asset_info["timeframe"],
        "trend": trend,
        "signal": signal,
        "confidence": confidence,
        "risk": risk,
        "whale_hint": whale_hint
    }
