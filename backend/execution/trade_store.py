from collections import defaultdict
from datetime import datetime

USER_TRADES = defaultdict(list)

def save_trade(user_id, trade):
    trade["timestamp"] = datetime.utcnow().isoformat()
    USER_TRADES[user_id].append(trade)

def get_user_trades(user_id, limit=50):
    return USER_TRADES[user_id][-limit:]

def get_all_trades(user_id):
    return USER_TRADES[user_id]
