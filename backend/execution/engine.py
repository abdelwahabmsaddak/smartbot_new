from backend.execution.trade_store import save_trade

def run_auto_trade(signal, account, user_id="demo"):
    # مثال تنفيذ
    result = {
        "asset": signal["asset"],
        "side": signal["side"],
        "entry": signal["entry"],
        "confidence": signal["confidence"],
        "mode": account.get("mode", "paper"),
        "pnl": round(signal.get("expected_pnl", 0), 2)
    }

    save_trade(user_id, result)
    return result
