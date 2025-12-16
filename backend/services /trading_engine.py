from backend.services.risk_manager import risk_check
from backend.services.exchange_factory import ExchangeExecutor

def run_auto_trade(signal, account):
    """
    signal = {
      action, entry, stop_loss, take_profit
    }
    """

    if signal["action"] not in ["BUY", "SELL"]:
        return {"status": "IGNORED"}

    qty = risk_check(
        balance=account["balance"],
        risk_percent=account["risk"],
        entry=signal["entry"],
        stop_loss=signal["stop_loss"]
    )

    if not qty:
        return {"status": "INVALID_RISK"}

    order = {
        "symbol": account["symbol"],
        "side": signal["action"],
        "entry": signal["entry"],
        "stop_loss": signal["stop_loss"],
        "take_profit": signal["take_profit"],
        "quantity": qty
    }

    executor = ExchangeExecutor(mode=account["mode"])
    return executor.execute(order)
