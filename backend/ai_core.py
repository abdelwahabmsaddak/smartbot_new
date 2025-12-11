from openai import OpenAI

client = OpenAI()

def ai_chat(prompt: str, system_msg="You are a helpful assistant."):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"
