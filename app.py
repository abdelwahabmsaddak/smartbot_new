from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")


# API لتحليل العملات / الذهب / الأسهم (placeholder)
@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    asset_type = data.get("type")   # crypto / gold / stock
    symbol = data.get("symbol")     # BTC, XAUUSD, AAPL ...
    # هنا تحط منطق التحليل الحقيقي لاحقاً
    fake_result = {
        "symbol": symbol,
        "type": asset_type,
        "summary": f"تحليل مبدئي لـ {symbol} ({asset_type}) سيتم تطويره لاحقاً."
    }
    return jsonify(fake_result)


# API للدردشة (placeholder)
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    # هنا تحط منطق الرد الحقيقي لاحقاً
    reply = "تم استلام رسالتك، سيتم إضافة منطق دردشة متقدم لاحقاً."
    return jsonify({"reply": reply})


# Endpoint بسيط لما يرجع PayPal بنجاح
@app.route("/paypal/success", methods=["GET"])
def paypal_success():
    # في النسخة المتقدمة: تتحقق من الدفع عبر Webhook أو API
    return "Payment received. Thank you!"


if __name__ == "__main__":
    app.run(debug=True)
