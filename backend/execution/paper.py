import time
import uuid
from backend.execution.trade_store import save_trade

# حالة Paper Account
PAPER_STATE = {
    "balance": 10000.0
}

def paper_execute_trade(user_id: str, signal: dict):
    """
    signal مثال:
    {
        "asset": "BTC/USDT",
        "side": "BUY",
        "entry": 42000,
        "exit": 42300,
        "confidence": 82
    }
    """

    trade_id = str(uuid.uuid4())

    entry = float(signal["entry"])
    exit_price = float(signal["exit"])
    side = signal["side"]

    # حساب PnL
    if side == "BUY":
        pnl = exit_price - entry
    else:
        pnl = entry - exit_price

    trade = {
        "id": trade_id,
        "asset": signal["asset"],
        "side": side,
        "entry": entry,
        "exit": exit_price,
        "pnl": round(pnl, 2),
        "mode": "paper"
    }

    # 🔥 أهم سطر في المشروع
    save_trade(user_id, trade)

    return {
        "status": "EXECUTED",
        "trade": trade
    }
