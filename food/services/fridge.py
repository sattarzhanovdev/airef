from food.models import Product, FridgeItem

def add_to_fridge(name, quantity="1 шт", category="Другое"):
    product, _ = Product.objects.get_or_create(
        name=name,
        defaults={"category": category}
    )

    item, created = FridgeItem.objects.get_or_create(
        product=product,
        defaults={"quantity": quantity}
    )

    if not created:
        item.quantity += f" + {quantity}"
        item.save()

    return item
