import os
from openai import OpenAI

def get_client():
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN environment variable is not set")

    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=token,
    )


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

def stream_food_answer(user_message, fridge_items):
    client = get_client()   # ← создаём ТУТ, а не при импорте

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
        model="openai/gpt-oss-120b:groq",
        messages=messages,
        stream=True,
    )
