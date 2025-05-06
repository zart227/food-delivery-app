# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order
from .serializers import OrderSerializer
from .tasks import send_order_confirmation_email
from basket.models import Basket
from utils.cache import cache_response, invalidate_cache_pattern
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class CreateOrderView(generics.CreateAPIView):
    """
    API endpoint для создания нового заказа.
    После создания заказа корзина пользователя очищается и отправляется email с подтверждением.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать новый заказ на основе текущей корзины пользователя",
        request_body=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: 'Неверные данные заказа'
        }
    )
    def perform_create(self, serializer):
        """
        Создание заказа с дополнительной логикой.
        
        Args:
            serializer: Сериализатор заказа
            
        Side effects:
            - Очищает корзину пользователя
            - Отправляет email с подтверждением заказа
            - Инвалидирует кеш корзины и заказов
            - Отправляет WebSocket уведомление
        """
        # Сохраняем заказ
        order = serializer.save()

        # Очищаем корзину для текущего пользователя
        Basket.objects.filter(user=self.request.user).delete()

        # Инвалидируем кеш корзины и заказов
        invalidate_cache_pattern('basket')
        invalidate_cache_pattern('orders')

        # Отправляем письмо с подтверждением
        send_order_confirmation_email.delay(order.id, self.request.user.email)

        # Отправляем WebSocket уведомление
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{self.request.user.id}_orders",
            {
                'type': 'order_status_update',
                'order_id': order.id,
                'status': order.status
            }
        )


class UpdateOrderStatusView(APIView):
    """
    API endpoint для обновления статуса заказа.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Обновить статус заказа",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['pending', 'processing', 'completed']
                )
            },
            required=['status']
        ),
        responses={
            200: OrderSerializer,
            400: 'Неверный статус',
            404: 'Заказ не найден'
        }
    )
    def patch(self, request, order_id):
        """
        Обновление статуса заказа.
        
        Args:
            order_id: ID заказа
            request.data: Новый статус заказа
        """
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            new_status = request.data.get('status')
            
            if new_status not in ['pending', 'processing', 'completed']:
                return Response(
                    {'error': 'Invalid status'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = new_status
            order.save()

            # Отправляем WebSocket уведомление
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}_orders",
                {
                    'type': 'order_status_update',
                    'order_id': order.id,
                    'status': order.status
                }
            )

            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ListOrdersView(generics.ListAPIView):
    """
    API endpoint для получения списка заказов текущего пользователя.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Получить список заказов текущего пользователя",
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
