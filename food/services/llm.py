import os
from openai import OpenAI

SYSTEM_PROMPT = """
Ты — AI Food Assistant.

ПРАВИЛА:
- Говори только про еду
- Используй ТОЛЬКО продукты из холодильника
- НЕ добавляй ингредиенты
- 2–3 блюда
- Укажи время приготовления
- Короткие шаги
- Ты не врач и не несёшь ответственности
"""

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def stream_food_answer(user_message, fridge_items):
    client = get_client()
    if not client:
        return None   # ❗ НИКАКИХ raise

    fridge_text = ", ".join(fridge_items) or "Холодильник пуст"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
Продукты в холодильнике:
{fridge_text}

Запрос:
{user_message}
"""
        }
    ]

    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )
