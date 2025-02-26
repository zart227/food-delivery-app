from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Basket
from .serializers import BasketSerializer
from utils.cache import CachedAPIView, invalidate_cache_pattern


class BasketView(CachedAPIView):
    """
    API endpoint для управления корзиной пользователя.
    Позволяет просматривать, добавлять, удалять и изменять количество товаров в корзине.
    """
    permission_classes = [IsAuthenticated]
    cache_key_prefix = 'basket'
    cache_timeout = 300  # 5 минут для корзины

    @swagger_auto_schema(
        operation_description="Получить содержимое корзины текущего пользователя",
        responses={200: BasketSerializer(many=True)}
    )
    def get(self, request):
        """
        Получение корзины текущего пользователя.
        
        Returns:
            Response: Список товаров в корзине пользователя
        """
        basket = Basket.objects.filter(user=request.user)
        serializer = BasketSerializer(basket, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        self.cache_response(request, response)
        return response

    @swagger_auto_schema(
        operation_description="Добавить товар в корзину",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID продукта'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество')
            },
            required=['product']
        ),
        responses={
            201: BasketSerializer,
            400: 'Неверные данные запроса'
        }
    )
    def post(self, request):
        """
        Добавление товара в корзину.
        
        Args:
            request.data: Словарь с данными товара (product_id и quantity)
            
        Returns:
            Response: Информация о добавленном товаре
        """
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = BasketSerializer(data=data)
        if serializer.is_valid():
            basket_item, created = Basket.objects.get_or_create(
                user=request.user,
                product_id=data["product"],
                defaults={"quantity": data.get("quantity", 1)},
            )
            if not created:
                basket_item.quantity += data.get("quantity", 1)
                basket_item.save()

            # Инвалидируем кеш корзины пользователя
            self.invalidate_cache(request)
            return Response(
                BasketSerializer(basket_item).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Удалить товар из корзины",
        responses={
            204: 'Товар успешно удален',
            404: 'Товар не найден в корзине'
        }
    )
    def delete(self, request, pk):
        """
        Удаление товара из корзины.
        
        Args:
            pk (int): ID записи в корзине
            
        Returns:
            Response: Статус операции
        """
        try:
            basket_item = Basket.objects.get(user=request.user, pk=pk)
            basket_item.delete()
            # Инвалидируем кеш корзины пользователя
            self.invalidate_cache(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Basket.DoesNotExist:
            return Response(
                {"error": "Item not found in your basket"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Обновить количество товара в корзине",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Новое количество')
            },
            required=['quantity']
        ),
        responses={
            200: BasketSerializer,
            400: 'Неверное количество',
            404: 'Товар не найден в корзине'
        }
    )
    def patch(self, request, pk):
        """
        Обновление количества товара в корзине.
        
        Args:
            pk (int): ID записи в корзине
            request.data: Словарь с новым количеством товара
            
        Returns:
            Response: Обновленная информация о товаре в корзине
        """
        try:
            basket_item = Basket.objects.get(user=request.user, pk=pk)
            new_quantity = request.data.get("quantity")
            if new_quantity is not None and int(new_quantity) > 0:
                basket_item.quantity = int(new_quantity)
                basket_item.save()
                # Инвалидируем кеш корзины пользователя
                self.invalidate_cache(request)
                return Response(
                    BasketSerializer(basket_item).data, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Basket.DoesNotExist:
            return Response(
                {"error": "Item not found in your basket"},
                status=status.HTTP_404_NOT_FOUND,
            )
