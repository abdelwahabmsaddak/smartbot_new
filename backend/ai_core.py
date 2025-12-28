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
