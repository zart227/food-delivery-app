from rest_framework import serializers
from django.conf import settings
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    image = serializers.SerializerMethodField()

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
