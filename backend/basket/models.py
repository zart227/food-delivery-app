from django.db import models
from django.conf import settings  # Импорт для AUTH_USER_MODEL
from products.models import Product  # Предполагается, что продукт определен в этом приложении


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="baskets",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="baskets")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} x {self.quantity}"
