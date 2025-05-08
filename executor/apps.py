from django.apps import AppConfig
from django_q.models import Schedule

class ExecutorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'executor'
