from flask import Blueprint, request, jsonify
from backend.execution.engine import execute

execute_bp = Blueprint("execute_bp", __name__)

@execute_bp.route("/execute_trade", methods=["POST"])
def execute_trade():
    """
    Body مثال:
    {
      "mode": "paper" أو "live",
      "exchange": "binance" أو "bybit" أو "okx"...
      "api_key": "...", "api_secret": "...", "password": null,
      "symbol": "BTC/USDT",
      "side": "BUY",
      "type": "MARKET",
      "quantity": 0.01,
      "price": null
    }
    """
    data = request.get_json() or {}

    try:
        mode = data.get("mode", "paper")
        exchange = data.get("exchange", "binance")

        api_key = data.get("api_key")
        api_secret = data.get("api_secret")
        password = data.get("password")

        symbol = data.get("symbol")
        side = data.get("side", "BUY")
        order_type = data.get("type", "MARKET")
        quantity = float(data.get("quantity", 0))
        price = data.get("price", None)
        if price is not None:
            price = float(price)

        if not symbol or quantity <= 0:
            return jsonify({"error": "symbol and quantity are required"}), 400

        out = execute(
            mode=mode,
            exchange=exchange,
            api_key=api_key,
            api_secret=api_secret,
            password=password,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        return jsonify({"status": "success", **out})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
