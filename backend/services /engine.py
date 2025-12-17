LIVE_TRADES = []

def record_trade(trade):
    LIVE_TRADES.append(trade)

def get_live_trades():
    return LIVE_TRADES[-20:]  # آخر 20 صفقة

def get_stats(trades):
    pnl = sum(t.get("pnl", 0) for t in trades)
    wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
    losses = sum(1 for t in trades if t.get("pnl", 0) < 0)

    return {
        "total_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "pnl": round(pnl, 2)
    }
