from flask import Blueprint, request, jsonify
from backend.services.ai_client import get_ai_client
from backend.services.ai_prompts import ai_signal_prompt

ai_signals_bp = Blueprint(
    "ai_signals",
    __name__,
    url_prefix="/api/ai-signals"
)

@ai_signals_bp.route("/analyze", methods=["POST"])
def analyze_signal():
    try:
        data = request.get_json()

        asset = data.get("asset")          # BTC/USDT, XAUUSD, AAPL
        timeframe = data.get("timeframe")  # 15m, 1h, 4h, 1d
        market = data.get("market")        # crypto | stock | gold

        if not all([asset, timeframe, market]):
            return jsonify({"error": "Missing parameters"}), 400

        client = get_ai_client()

        prompt = ai_signal_prompt(asset, timeframe, market)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت محلل تداول ذكي"},
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({
            "asset": asset,
            "timeframe": timeframe,
            "market": market,
            "signal": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
