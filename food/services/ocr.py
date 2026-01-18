import pytesseract
from PIL import Image


def extract_text_from_image(image_file) -> str:
    """
    Принимает InMemoryUploadedFile
    Возвращает распознанный текст
    """
    image = Image.open(image_file)

    text = pytesseract.image_to_string(
        image,
        lang="rus",
        config="--oem 3 --psm 6"
    )

    return text
