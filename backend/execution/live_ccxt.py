import ccxt

class LiveCCXTExecutor:
    def __init__(self, exchange_name: str, api_key: str, api_secret: str, password: str | None = None):
        exchange_class = getattr(ccxt, exchange_name, None)
        if exchange_class is None:
            raise ValueError(f"Unsupported exchange: {exchange_name}")

        cfg = {
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        }
        if password:
            cfg["password"] = password

        self.exchange = exchange_class(cfg)

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float | None = None):
        side = side.lower()
        order_type = order_type.lower()

        if order_type == "market":
            return self.exchange.create_order(symbol, "market", side, quantity)
        elif order_type == "limit":
            if price is None:
                raise ValueError("Limit order requires price")
            return self.exchange.create_order(symbol, "limit", side, quantity, price)
        else:
            raise ValueError("order_type must be MARKET or LIMIT")
