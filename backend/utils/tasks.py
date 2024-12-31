from celery import shared_task
from django.contrib.sessions.models import Session
from datetime import datetime


@shared_task
def clear_expired_sessions():
    """
    Удаляет устаревшие сессии из базы данных Django.
    """
    expired_sessions = Session.objects.filter(expire_date__lt=datetime.now())
    count = expired_sessions.count()  # Считаем количество удаляемых сессий
    expired_sessions.delete()
    return f"Удалено {count} устаревших сессий."


@shared_task
def test_task():
    print("Celery is working!")
