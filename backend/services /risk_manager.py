def risk_check(balance, risk_percent, entry, stop_loss):
    risk_amount = balance * (risk_percent / 100)
    loss_per_unit = abs(entry - stop_loss)

    if loss_per_unit <= 0:
        return None

    quantity = risk_amount / loss_per_unit
    return round(quantity, 4)
