from rest_framework import serializers
from django.conf import settings
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(help_text="Название продукта")
    description = serializers.CharField(help_text="Описание продукта")
    price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Цена продукта")
    image = serializers.SerializerMethodField(help_text="URL изображения продукта")
    category = CategorySerializer(read_only=True, help_text="Категория продукта")
    category_id = serializers.IntegerField(write_only=True, help_text="ID категории продукта")
    is_available = serializers.BooleanField(help_text="Доступен ли продукт для заказа")
    weight = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, help_text="Вес в граммах")
    calories = serializers.IntegerField(required=False, help_text="Калорийность продукта")
    is_vegetarian = serializers.BooleanField(help_text="Вегетарианский продукт")
    is_spicy = serializers.BooleanField(help_text="Острый продукт")

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'image',
            'category', 'category_id', 'is_available', 'weight',
            'calories', 'is_vegetarian', 'is_spicy'
        ]

    def get_image(self, obj):
        # Если у объекта есть URL для изображения, добавляем полный URL
        if obj.image:
            # request = self.context.get('request')
            # if request:
            #     return request.build_absolute_uri(obj.image.url)
            # Если request недоступен, строим URL вручную
            return f"{settings.SITE_URL}{obj.image.url}"
        return None
