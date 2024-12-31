from rest_framework import serializers
from .models import Basket
from products.serializers import ProductSerializer
from products.models import Product


class BasketSerializer(serializers.ModelSerializer):
    # Для записи принимаем ID продукта, для чтения возвращаем объект
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_data = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'product', 'product_data', 'quantity']
        read_only_fields = ['user']
