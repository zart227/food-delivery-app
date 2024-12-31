# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from .models import Order
from .serializers import OrderSerializer
from .tasks import send_order_confirmation_email
from basket.models import Basket


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Сохраняем заказ
        order = serializer.save()

        # Очищаем корзину для текущего пользователя
        Basket.objects.filter(user=self.request.user).delete()

        # Отправляем письмо с подтверждением
        send_order_confirmation_email.delay(order.id, self.request.user.email)
