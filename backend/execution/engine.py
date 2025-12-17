from backend.execution.paper import paper_execute_trade
# لاحقًا: from backend.execution.live_ccxt import live_execute_trade

def run_trade(user_id: str, signal: dict, account: dict):
    """
    account:
    {
        "mode": "paper" | "live"
    }
    """

    mode = account.get("mode", "paper")

    if mode == "paper":
        return paper_execute_trade(user_id, signal)

    elif mode == "live":
        # 🔒 مقفولة مؤقتًا
        return {
            "status": "DISABLED",
            "reason": "Live trading not enabled yet"
        }

    else:
        raise ValueError("Invalid trading mode")
