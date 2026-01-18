from django.urls import path
from .views import (
    FoodChatStreamView,
    ReceiptView,
    FridgeView,
    ReceiptImageView,
)

urlpatterns = [
    path("chat/stream/", FoodChatStreamView.as_view()),
    path("receipt/text/", ReceiptView.as_view()),
    path("receipt/image/", ReceiptImageView.as_view()),
    path("fridge/", FridgeView.as_view()),
]