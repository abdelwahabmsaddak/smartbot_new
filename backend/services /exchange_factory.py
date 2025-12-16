class ExchangeExecutor:
    def __init__(self, mode="paper"):
        self.mode = mode

    def execute(self, order):
        if self.mode == "paper":
            return {
                "status": "SIMULATED",
                "order": order
            }

        # لاحقًا: Binance / Bybit / OKX
        return {"status": "LIVE_NOT_ENABLED"}
