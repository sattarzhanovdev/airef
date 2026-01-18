from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from food.models import FridgeItem
from food.services.llm import stream_food_answer
from food.services.receipt_parser import parse_receipt
from food.services.fridge import add_to_fridge
from rest_framework.parsers import MultiPartParser, FormParser
from food.services.ocr import extract_text_from_image
from food.services.receipt_llm_cleaner import extract_food_products_from_receipt


class FoodChatStreamView(APIView):
    def post(self, request):
        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "message required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        fridge_items = list(
            FridgeItem.objects.values_list("product__name", flat=True)
        )

        def stream():
            response = stream_food_answer(message, fridge_items)
            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

        return StreamingHttpResponse(
            stream(),
            content_type="text/plain; charset=utf-8"
        )


class ReceiptView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        products = parse_receipt(text)

        added = []
        for p in products:
            add_to_fridge(p)
            added.append(p)

        return Response({"added": added})


class FridgeView(APIView):
    def get(self, request):
        items = FridgeItem.objects.select_related("product")
        return Response([
            {
                "name": i.product.name,
                "quantity": i.quantity,
                "category": i.product.category,
            }
            for i in items
        ])


class ReceiptImageView(APIView):
    """
    OCR по фото чека + добавление продуктов в холодильник
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image = request.FILES.get("image")

        if not image:
            return Response(
                {"error": "image file required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. OCR
        text = extract_text_from_image(image)

        # 2. Парсим чек
        products = extract_food_products_from_receipt(text)

        # 3. Добавляем в холодильник
        added = []
        for product in products:
            add_to_fridge(product)
            added.append(product)

        return Response({
            "recognized_text": text,
            "added_products": added
        })
