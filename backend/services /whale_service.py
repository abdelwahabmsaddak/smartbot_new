import random
from db import get_db
from services.notification_service import create_notification

WHALE_THRESHOLD = 500_000  # 500k$

def detect_whale(asset="BTC", user_id=None):
    amount = random.randint(300_000, 5_000_000)
    if amount < WHALE_THRESHOLD:
        return None

    direction = random.choice(["IN", "OUT"])
    exchange = random.choice(["Binance", "Coinbase", "OKX"])

    db = get_db()
    db.execute("""
        INSERT INTO whale_alerts (asset, amount, direction, exchange)
        VALUES (?, ?, ?, ?)
    """, (asset, amount, direction, exchange))
    db.commit()

    # Notification
    if user_id:
        create_notification(
            user_id=user_id,
            title="🐋 Whale Alert",
            message=f"{asset} {direction} {amount:,.0f}$ on {exchange}",
            type="whale"
        )

    return {
        "asset": asset,
        "amount": amount,
        "direction": direction,
        "exchange": exchange
    }
