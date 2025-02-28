from django.db import migrations
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


def create_periodic_tasks(apps, schema_editor):
    # Создаем расписания
    interval_schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    # Создаем CRON расписания
    daily_midnight_cron, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='0',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    daily_cleanup_cron, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='3',  # В 3 часа ночи
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    # Создаем периодические задачи
    PeriodicTask.objects.get_or_create(
        name='Generate Daily Report',
        task='orders.tasks.generate_daily_report',
        crontab=daily_midnight_cron,
        enabled=True,
    )

    PeriodicTask.objects.get_or_create(
        name='Delete Old Pending Orders',
        task='orders.tasks.delete_old_pending_orders',
        interval=interval_schedule,
        enabled=True,
    )

    PeriodicTask.objects.get_or_create(
        name='Clear Expired Sessions',
        task='utils.tasks.clear_expired_sessions',
        crontab=daily_cleanup_cron,
        enabled=True,
    )


def delete_periodic_tasks(apps, schema_editor):
    # Удаляем все созданные задачи при откате миграции
    PeriodicTask.objects.filter(
        name__in=[
            'Generate Daily Report',
            'Delete Old Pending Orders',
            'Clear Expired Sessions',
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('django_celery_beat', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_periodic_tasks, delete_periodic_tasks),
    ] 