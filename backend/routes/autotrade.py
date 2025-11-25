from flask import Blueprint, request, jsonify
import threading, time
import yfinance as yf

autotrade_bp = Blueprint("autotrade_bp", __name__)

bot_running = False

def trading_bot(params):
    global bot_running
    symbol = params["symbol"]

    while bot_running:
        data = yf.download(symbol, period="1d", interval="1m")
        last = data["Close"].iloc[-1]

        # شروط التداول
        if last <= last * (1 - float(params["buy_drop"]) / 100):
            print("BUY SIGNAL")

        if last >= last * (1 + float(params["take_profit"]) / 100):
            print("SELL TAKE PROFIT")

        if last <= last * (1 - float(params["stop_loss"]) / 100):
            print("STOP LOSS SELL")

        time.sleep(20)  # كل 20 ثانية يراجع السوق

@autotrade_bp.route("/start_bot", methods=["POST"])
def start_bot():
    global bot_running
    bot_running = True

    params = request.json
    t = threading.Thread(target=trading_bot, args=(params,))
    t.start()

    return jsonify({"message": "تم تشغيل التداول الآلي بنجاح ✔️"})

@autotrade_bp.route("/stop_bot")
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"message": "تم إيقاف التداول الآلي ❌"})
