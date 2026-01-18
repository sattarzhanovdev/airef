from food.services.openai_client import get_openai_client

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
    client = get_openai_client()  # ← КЛЮЧЕВОЕ ИЗМЕНЕНИЕ

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

    return [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]
