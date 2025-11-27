import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class SmartAI:

    @staticmethod
    def chat(message):
        """ ذكاء اصطناعي للدردشة + التحليل السريع """
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message["content"]

    @staticmethod
    def analyze(symbol, timeframe="1h"):
        """ تحليل الأسواق — يستخدم في analysis + screener """
        prompt = f"""
        حلّل لي العملة/السهم التالي: {symbol}
        على الإطار: {timeframe}
        واربط التحليل بالاتجاه – الدعم – المقاومة – المؤشرات – الذكاء الاصطناعي.
        أعطيني النتيجة بشكل JSON:
        {{
            "trend": "",
            "support": "",
            "resistance": "",
            "prediction": "",
            "risk": "",
            "ai_signal": ""
        }}
        """
        return SmartAI.chat(prompt)

    @staticmethod
    def auto_trade_decision(symbol, balance):
        """ قرار التداول الآلي PRO """
        prompt = f"""
        نريد قرار تداول آلي احترافي.
        الأصل: {symbol}
        الرصيد: {balance}
        أعطني قرار JSON:
        {{
            "action": "buy/sell/wait",
            "confidence": "",
            "take_profit": "",
            "stop_loss": "",
            "reason": ""
        }}
        """
        return SmartAI.chat(prompt)

    @staticmethod
    def whale_analysis(data):
        """ تحليل عمليات الحيتان """
        prompt = f"""
        هذه بيانات حركة حيتان:
        {data}

        أعطني تحليل ذكاء اصطناعي:
        - هل الحركة إيجابية أم سلبية؟
        - هل هناك تجميع أو تصريف؟
        - تأثيرها على السعر المتوقع؟
        """
        return SmartAI.chat(prompt)

    @staticmethod
    def ai_blog_writer(topic):
        """ كتابة تدوينات بالذكاء الاصطناعي """
        prompt = f"اكتب مقالا احترافيا عن: {topic}"
        return SmartAI.chat(prompt)
