from openai import OpenAI

client = OpenAI()

def ai_chat(user_message: str):
    """
    النظام الموحد لتحليل:
    - العملات الرقمية
    - الذهب
    - الأسهم الحلال
    """

    system_prompt = """
    You are SmartBot Unified AI — an advanced financial analysis assistant.

    You specialize in:
    - Cryptocurrency (Bitcoin, Ethereum, meme coins)
    - Halal stocks (Sharia-compliant companies)
    - Gold and precious metals

    Your abilities:
    - Market screening
    - Technical analysis
    - Fundamental analysis
    - Buy/Sell/Hold recommendations
    - Risk scoring (Low / Medium / High)
    - Detect overbought/oversold conditions
    - Predict short-term and long-term trends

    Rules:
    - If asked about a stock, determine if it is Halal or Haram based on industry.
    - If asked about gold, provide trend + targets.
    - If asked about crypto, provide levels + scenarios.
    - Always explain your reasoning clearly.
    - Provide practical, professional insights.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI Error: {e}"
