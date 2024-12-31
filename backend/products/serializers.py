from rest_framework import serializers
from django.conf import settings
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "image"]

    def get_image(self, obj):
        # Если у объекта есть URL для изображения, добавляем полный URL
        if obj.image:
            # request = self.context.get('request')
            # if request:
            #     return request.build_absolute_uri(obj.image.url)
            # Если request недоступен, строим URL вручную
            return f"{settings.SITE_URL}{obj.image.url}"
        return None
