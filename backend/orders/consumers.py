import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Order


class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        # Проверяем аутентификацию
        if not self.user.is_authenticated:
            await self.close()
            return

        # Создаем уникальную комнату для пользователя
        self.room_group_name = f"user_{self.user.id}_orders"

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Отправляем текущие статусы заказов при подключении
        orders_statuses = await self.get_user_orders_statuses()
        await self.send(text_data=json.dumps({
            'type': 'orders_statuses',
            'statuses': orders_statuses
        }))

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Получение сообщений от клиента
        """
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'get_order_status':
                order_id = text_data_json.get('order_id')
                if order_id:
                    status = await self.get_order_status(order_id)
                    await self.send(text_data=json.dumps({
                        'type': 'order_status',
                        'order_id': order_id,
                        'status': status
                    }))
        except json.JSONDecodeError:
            pass

    async def order_status_update(self, event):
        """
        Отправка обновления статуса заказа клиенту
        """
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_id': event['order_id'],
            'status': event['status']
        }))

    @database_sync_to_async
    def get_order_status(self, order_id):
        """
        Получение статуса конкретного заказа
        """
        try:
            order = Order.objects.get(id=order_id, user=self.user)
            return order.status
        except Order.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user_orders_statuses(self):
        """
        Получение статусов всех заказов пользователя
        """
        orders = Order.objects.filter(user=self.user).values('id', 'status')
        return list(orders) 