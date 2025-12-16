def ai_signal_prompt(asset, timeframe, market_type):
    return f"""
أنت محلل تداول محترف.

حلل الأصل التالي:
- الأصل: {asset}
- الإطار الزمني: {timeframe}
- السوق: {market_type}

شروط:
- إذا كان سهم: يكون حلال (تجنّب البنوك، الكحول، القمار).
- أعطِ إشارة واضحة: BUY / SELL / HOLD
- حدّد:
  - Entry
  - Stop Loss
  - Take Profit
  - Confidence (0-100%)
- اختصر بدون حشو.

أجب بصيغة JSON فقط.
"""
