from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import Order, OrderItem
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(order_id, user_email):
    try:
        # Получаем заказ и его элементы
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        # Формируем текст письма с деталями заказа
        order_details = "\n".join(
            [
                f"{item.product.title} × {item.quantity} шт. — {item.price} ₽"
                for item in order_items
            ]
        )
        total_price = f"Общая стоимость: {order.total_price} ₽"

        message_body = (
            f"Ваш заказ #{order_id} успешно оформлен!\n\n"
            "Детали заказа:\n"
            f"{order_details}\n\n"
            f"{total_price}\n\n"
            "Спасибо за ваш заказ!"
        )

        # Отправляем письмо
        send_mail(
            subject="Ваш заказ оформлен",
            message=message_body,
            from_email="noreply@example.com",
            recipient_list=[user_email],
        )
        print(f"Email отправлен на {user_email}")
    except Order.DoesNotExist:
        print(f"Ошибка: Заказ с ID {order_id} не найден.")
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")


@shared_task
def delete_old_pending_orders():
    threshold_date = now() - timedelta(days=7)
    old_orders = Order.objects.filter(status="pending", created_at__lt=threshold_date)
    count = old_orders.count()
    old_orders.delete()
    return f"Deleted {count} old pending orders."


@shared_task
def generate_daily_report():
    from django.db.models import Sum

    today = now().date()
    completed_orders = Order.objects.filter(status="completed", created_at__date=today)
    total_revenue = completed_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = completed_orders.count()

    send_mail(
        subject="Ежедневный отчет о заказах",
        message=f"Сегодня выполнено заказов: {total_orders}\nОбщая выручка: {total_revenue} ₽",
        from_email="noreply@example.com",
        recipient_list=["admin@example.com"],
    )
    return f"Generated daily report: {total_orders} orders, {total_revenue} ₽ revenue."
