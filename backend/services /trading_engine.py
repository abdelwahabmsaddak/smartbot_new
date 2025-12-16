from backend.services.risk_manager import risk_check
from backend.services.exchange_factory import ExchangeExecutor

def run_auto_trade(signal: dict, account: dict):
    action = signal.get("action", "HOLD")
    if action not in ["BUY", "SELL"]:
        return {"status": "IGNORED", "reason": "Signal is HOLD or invalid"}

    entry = float(signal.get("entry", 0) or 0)
    sl = float(signal.get("stop_loss", 0) or 0)
    tps = signal.get("take_profit", [])
    tp1 = float(tps[0]) if isinstance(tps, list) and len(tps) else None

    qty = risk_check(
        balance=float(account.get("balance", 0)),
        risk_percent=float(account.get("risk", 1)),
        entry=entry,
        stop_loss=sl
    )
    if not qty:
        return {"status": "INVALID_RISK", "reason": "Bad entry/SL or zero risk distance"}

    order = {
        "symbol": account.get("symbol"),
        "side": action,
        "type": account.get("type", "MARKET"),
        "quantity": qty,
        "entry": entry,
        "stop_loss": sl,
        "take_profit": tp1,
        "timeframe": account.get("timeframe"),
        "exchange": account.get("exchange"),
    }

    executor = ExchangeExecutor(mode=account.get("mode", "paper"))
    return executor.execute(order)
