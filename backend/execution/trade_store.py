from collections import defaultdict
from datetime import datetime

# مخزن في الذاكرة (لاحقًا نبدلوه DB)
USER_TRADES = defaultdict(list)

REQUIRED_FIELDS = [
    "asset", "side", "entry", "exit", "pnl", "mode"
]

def save_trade(user_id: str, trade: dict):
    # حماية من trade ناقص
    for field in REQUIRED_FIELDS:
        if field not in trade:
            raise ValueError(f"Missing trade field: {field}")

    trade_record = {
        "id": trade.get("id"),
        "asset": trade["asset"],
        "side": trade["side"],           # BUY / SELL
        "entry": float(trade["entry"]),
        "exit": float(trade["exit"]),
        "pnl": float(trade["pnl"]),
        "mode": trade.get("mode", "paper"),
        "timestamp": datetime.utcnow().isoformat()
    }

    USER_TRADES[user_id].append(trade_record)
    return trade_record


def get_user_trades(user_id: str, limit: int = 10):
    return USER_TRADES[user_id][-limit:]


def get_all_trades(user_id: str):
    return USER_TRADES[user_id]


def get_stats(user_id: str):
    trades = USER_TRADES[user_id]

    total = len(trades)
    wins = len([t for t in trades if t["pnl"] > 0])
    losses = len([t for t in trades if t["pnl"] <= 0])
    pnl = round(sum(t["pnl"] for t in trades), 2)

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "pnl": pnl
    }
