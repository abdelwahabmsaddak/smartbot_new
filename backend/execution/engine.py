from backend.execution.paper import paper_place_order, paper_state
from backend.execution.live_ccxt import LiveCCXTExecutor

def execute(mode: str, exchange: str, api_key: str | None, api_secret: str | None, password: str | None,
            symbol: str, side: str, order_type: str, quantity: float, price: float | None):
    mode = (mode or "paper").lower()

    if mode == "paper":
        trade = paper_place_order(symbol, side, order_type, quantity, price)
        return {"mode": "paper", "result": trade, "paper_state": paper_state()}

    if mode == "live":
        if not api_key or not api_secret:
            raise ValueError("LIVE mode requires api_key and api_secret")

        executor = LiveCCXTExecutor(exchange_name=exchange, api_key=api_key, api_secret=api_secret, password=password)
        result = executor.place_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price)
        return {"mode": "live", "result": result}

    raise ValueError("mode must be 'paper' or 'live'")
