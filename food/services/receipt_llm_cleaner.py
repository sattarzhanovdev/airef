from openai import OpenAI
import os

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),
)

SYSTEM_PROMPT = """
Ты — помощник по очистке чеков.

Твоя задача:
- Из текста чека выделить ТОЛЬКО товары питания
- Исключить:
  • магазины
  • адреса
  • документы
  • табачные изделия
  • алкоголь
  • банки и платежи
  • акции и баллы

Верни результат СТРОГО в формате:
Товар 1
Товар 2
Товар 3

Без комментариев.
"""

def extract_food_products_from_receipt(raw_text: str) -> list[str]:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:groq",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Текст чека:\n{raw_text}"
            }
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    products = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    return products
