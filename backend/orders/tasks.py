from celery import shared_task
from datetime import date, datetime, time, timedelta
from django.utils import timezone
from django.utils.timezone import now
from .models import Order, OrderItem
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_order_confirmation_email(order_id, user_email):
    try:
        # Получаем заказ и его элементы с подгрузкой товаров
        order = Order.objects.prefetch_related('items__product').get(id=order_id)
        # Формируем контекст для шаблона
        context = {
            "order": order,
            "site_name": "Ваш сайт",  # Можно заменить на Site.objects.get_current().name
        }
        subject = f"Ваш заказ #{order.id} успешно оформлен!"
        text_content = f"Ваш заказ #{order.id} успешно оформлен!"
        # text_content = render_to_string("email/order_success.html", context)
        html_content = render_to_string("email/order_success.html", context)
        msg = EmailMultiAlternatives(subject, text_content, "noreply@example.com", [user_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
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
def generate_daily_report(report_date: date | None = None):
    """Report completed orders created during a local calendar day."""
    from django.db.models import Sum

    report_timezone = timezone.get_default_timezone()
    if report_date is None:
        report_date = timezone.localdate(timezone=report_timezone) - timedelta(days=1)
    # ISO dates also allow manual recalculation through Celery's JSON serializer.
    elif isinstance(report_date, str):
        report_date = date.fromisoformat(report_date)
    start = datetime.combine(report_date, time.min, tzinfo=report_timezone)
    end = datetime.combine(report_date + timedelta(days=1), time.min, tzinfo=report_timezone)
    # Order has no completion timestamp; use its creation time and current status.
    completed_orders = Order.objects.filter(
        status="completed", created_at__gte=start, created_at__lt=end,
    )
    total_revenue = completed_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = completed_orders.count()

    send_mail(
        subject=f"Ежедневный отчет о заказах за {report_date:%Y-%m-%d}",
        message=(f"Отчет за {report_date:%Y-%m-%d}\n"
                 f"Выполнено заказов: {total_orders}\nОбщая выручка: {total_revenue} ₽"),
        from_email="noreply@example.com",
        recipient_list=["admin@example.com"],
    )
    return f"Generated daily report: {total_orders} orders, {total_revenue} ₽ revenue."
