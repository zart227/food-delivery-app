import os
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запуск Celery worker'

    def handle(self, *args, **kwargs):
        # Указываем настройки для Celery
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

        # Команда для запуска Celery worker
        worker_command = ['celery', '-A', 'backend', 'worker', '--loglevel=info']

        # Выполняем команду в subprocess
        self.stdout.write('Запуск Celery worker...')
        subprocess.call(worker_command)
