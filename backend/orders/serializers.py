from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "product_detail", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    address = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=15)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "created_at",
            "total_price",
            "address",
            "phone",
            "notes",
            "items",
        ]
        read_only_fields = ["user"]  # Поле `user` только для чтения

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user  # Получаем текущего пользователя из контекста

        # Создаем заказ
        order = Order.objects.create(user=user, **validated_data)

        # Создаем элементы заказа
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        # Импортируем необходимые классы для отправки письма
        from users.email import OrderConfirmationEmail
        from django.contrib.sites.models import Site
        from django.conf import settings

        current_site = Site.objects.get_current()
        protocol = "https" if getattr(settings, 'SECURE_SSL_REDIRECT', False) else "http"
        OrderConfirmationEmail(
            context={
                "user": order.user,
                "order": order,
                "site_name": current_site.name,
                "domain": current_site.domain,
                "protocol": protocol,
                "delivery_address": order.address,
                "order_status_display": order.get_status_display(),
            }
        ).send([order.user.email])

        return order
