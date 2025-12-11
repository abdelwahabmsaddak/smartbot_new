import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def ai_chat(user_message: str) -> str:
    """
    دالّة الدردشة مع الذكاء الاصطناعي.
    ترجع رسالة واضحة لو OPENAI_API_KEY غير موجود.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "⚠️ لم يتم ضبط مفتاح OPENAI_API_KEY في إعدادات Render."

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message},
            ],
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ AI Error: {e}"
