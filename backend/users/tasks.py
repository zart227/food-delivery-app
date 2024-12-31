# Например, users/tasks.py
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_email(user_id):
    from users.models import User

    user = User.objects.get(pk=user_id)
    # Логика отправки письма
    print(f"Отправлено письмо для пользователя {user.email}")


@shared_task
def send_welcome_email(user_email):
    send_mail(
        subject="Добро пожаловать!",
        message="Спасибо за регистрацию на нашем сайте. Мы рады видеть вас!",
        from_email="noreply@example.com",
        recipient_list=[user_email],
    )
    print(f"Отправлено письмо для пользователя {user_email}")
