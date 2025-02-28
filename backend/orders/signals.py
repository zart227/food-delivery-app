from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from users.email import OrderConfirmationEmail

@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    """
    Отправляет письмо с подтверждением заказа
    """
    if created:
        OrderConfirmationEmail(
            context={
                "user": instance.user,
                "order": instance
            }
        ).send([instance.user.email]) 