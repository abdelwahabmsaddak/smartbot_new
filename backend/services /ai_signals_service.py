def generate_signal(asset, timeframe, market, halal_strict=True):
    """
    Output موحّد وقياسي
    """
    signal = {
        "asset": asset,
        "timeframe": timeframe,
        "market": market,
        "side": "BUY",
        "confidence": 78,
        "entry": 43250,
        "tp": 44500,
        "sl": 42600,
        "expected_pnl": 3.2,
        "halal": True
    }

    if halal_strict and not signal["halal"]:
        return None

    return signal
