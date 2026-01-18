from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FridgeItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
