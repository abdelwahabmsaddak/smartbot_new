from collections import defaultdict
from datetime import datetime

USER_TRADES = defaultdict(list)

def save_trade(user_id: str, trade: dict):
    trade = dict(trade)
    trade["timestamp"] = datetime.utcnow().isoformat()
    USER_TRADES[user_id].append(trade)
    return trade

def get_user_trades(user_id: str, limit: int = 50):
    return USER_TRADES[user_id][-limit:]

def get_all_trades(user_id: str):
    return USER_TRADES[user_id]

def get_stats(trades: list):
    total = len(trades)
    wins = 0
    losses = 0
    pnl = 0.0

    for t in trades:
        # توقع أن trade فيها pnl (موجب ربح / سالب خسارة)
        tpnl = float(t.get("pnl", 0) or 0)
        pnl += tpnl
        if tpnl > 0:
            wins += 1
        elif tpnl < 0:
            losses += 1

    return {
        "totalTrades": total,
        "wins": wins,
        "losses": losses,
        "pnl": round(pnl, 4)
    }
