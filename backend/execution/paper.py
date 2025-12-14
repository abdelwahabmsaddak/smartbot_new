import time
import uuid

# “محفظة” بسيطة في الذاكرة (تنجم لاحقًا تربطها بSQLite)
PAPER_STATE = {
    "balances": {"USD": 10000.0},
    "positions": {},  # مثال: {"BTCUSDT": {"qty": 0.01, "avg": 40000}}
    "trades": []
}

def paper_place_order(symbol: str, side: str, order_type: str, quantity: float, price: float | None = None):
    trade_id = str(uuid.uuid4())
    ts = int(time.time())

    # ملاحظة: بدون أسعار حقيقية — إذا ما عطيتش price نخليها 0 كـ placeholder
    exec_price = float(price) if price is not None else 0.0

    trade = {
        "id": trade_id,
        "timestamp": ts,
        "symbol": symbol,
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": float(quantity),
        "price": exec_price,
        "mode": "paper",
        "status": "filled"
    }

    PAPER_STATE["trades"].append(trade)
    return trade


def paper_state():
    return PAPER_STATE
