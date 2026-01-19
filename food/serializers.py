from rest_framework import serializers
from .models import FridgeItem


class FridgeItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")
    category = serializers.CharField(source="product.category")

    class Meta:
        model = FridgeItem
        fields = ["id", "name", "category", "quantity"]
