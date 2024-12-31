from django.db import migrations


def create_clear_sessions_task(apps, schema_editor):
    # Получаем модели IntervalSchedule и PeriodicTask
    IntervalSchedule = apps.get_model("django_celery_beat", "IntervalSchedule")
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")

    # Создаём или получаем расписание (раз в день)
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period="days",  # Используем строку вместо IntervalSchedule.DAYS
    )

    # Создаём задачу, если её ещё нет
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Clear Expired Sessions",  # Уникальное имя задачи
        task="utils.tasks.clear_expired_sessions",  # Полное имя задачи
    )


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(create_clear_sessions_task),
    ]
