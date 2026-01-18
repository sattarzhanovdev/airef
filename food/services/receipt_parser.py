import re

STOP_WORDS = [
    "инн", "ккт", "касс", "итог", "ндс", "налич",
    "получено", "сайт", "фн", "фп", "осо",
    "чек", "адрес", "улица", "город", "рн",
    "место", "расчет", "офис", "дата",
]

def looks_like_product(line: str) -> bool:
    line = line.lower().strip()

    if len(line) < 3:
        return False

    # отбрасываем строки, где почти одни цифры
    digits = len(re.findall(r"\d", line))
    letters = len(re.findall(r"[a-zа-яё]", line, re.IGNORECASE))

    if letters < 3:
        return False

    if digits > letters:
        return False

    for word in STOP_WORDS:
        if word in line:
            return False

    return True


def clean_product_name(line: str) -> str:
    # оставляем кириллицу, латиницу, цифры, дефисы
    line = re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9\s\-\"']", "", line)
    return re.sub(r"\s{2,}", " ", line).strip().title()


def parse_receipt(text: str) -> list[str]:
    products = []

    for raw_line in text.splitlines():
        if looks_like_product(raw_line):
            name = clean_product_name(raw_line)
            if name:
                products.append(name)

    return list(dict.fromkeys(products))
