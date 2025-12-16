def ai_signal_prompt(asset, timeframe, market_type):
    return f"""
حلّل الأصل التالي وارجع النتيجة بصيغة JSON فقط:

- asset: {asset}
- timeframe: {timeframe}
- market: {market_type}  (crypto | gold | stock)

JSON المطلوب بالضبط:
{{
  "action": "BUY|SELL|HOLD",
  "entry": number,
  "stop_loss": number,
  "take_profit": [number, number],
  "confidence": 0-100,
  "notes": "short reason"
}}

قواعد:
- إذا ما عندكش ثقة أو الداتا غير كافية → HOLD
- خليك واقعي ومحافظ.
"""
