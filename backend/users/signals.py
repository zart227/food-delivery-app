from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_activated
from .models import User, Role, UserRole
from .tasks import send_welcome_email
from djoser.email import ActivationEmail
from django.contrib.auth import get_user_model
from .email import WelcomeEmail

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    """
    Сигнал для назначения роли по умолчанию и отправки письма активации.
    """
    if created:  # Если пользователь только что создан
        try:
            default_role = Role.objects.get(name="Default")
        except Role.DoesNotExist:
            default_role = Role.objects.create(name="Default", description="Роль по умолчанию")

        UserRole.objects.create(user=instance, role=default_role)

        # Отправляем письмо активации
        if not instance.is_active:  # Проверяем, что пользователь неактивен
            try:
                email = ActivationEmail({"request": None}, context={"user": instance})
                email.send([instance.email])
            except Exception as e:
                print(f"Ошибка отправки письма активации: {e}")


@receiver(user_activated)
def send_welcome_email_after_activation(user, request, **kwargs):
    """
    Отправляет приветственное письмо после активации аккаунта.
    """
    try:
        WelcomeEmail(context={"user": user}).send([user.email])
    except Exception as e:
        print(f"Ошибка при отправке приветственного письма: {e}")
