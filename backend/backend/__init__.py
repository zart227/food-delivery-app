from __future__ import absolute_import, unicode_literals

# Это позволяет использовать Celery как часть Django
from .celery import app as celery_app

__all__ = ('celery_app',)
