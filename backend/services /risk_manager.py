def validate_signal(signal, min_confidence=60):
    if not signal:
        return False, "NO_SIGNAL"

    if signal["confidence"] < min_confidence:
        return False, "LOW_CONFIDENCE"

    if signal["sl"] >= signal["entry"]:
        return False, "INVALID_SL"

    return True, "OK"
