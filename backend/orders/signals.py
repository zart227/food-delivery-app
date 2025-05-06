from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from users.email import OrderConfirmationEmail
from django.contrib.sites.models import Site
from django.conf import settings

@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    """
    Отправляет письмо с подтверждением заказа
    """
    if created:
        # Получаем заказ с подгруженными товарами
        # print(f"Order ID: {instance.id}")
        # print(f"User Email: {instance.user.email}")
        # print(f"Items: {instance.items}")
        # print(instance.items.product)
        order = Order.objects.prefetch_related('items__product').get(id=instance.id)
        current_site = Site.objects.get_current()
        protocol = "https" if getattr(settings, 'SECURE_SSL_REDIRECT', False) else "http"
        OrderConfirmationEmail(
            context={
                "user": order.user,
                "order": order,
                "site_name": current_site.name,
                "domain": current_site.domain,
                "protocol": protocol,
                "delivery_address": order.address,
                "order_status_display": order.get_status_display(),
            }
        ).send([order.user.email]) 