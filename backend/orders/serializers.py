from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


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

        return order
