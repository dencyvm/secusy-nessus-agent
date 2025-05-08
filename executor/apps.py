from django.apps import AppConfig
from django_q.models import Schedule

class ExecutorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'executor'

    def ready(self):
        from nessusEngine.health_check import run_health_check
        Schedule.objects.update_or_create(
            name='daily_health_check',
            defaults={
                'func': 'nessusEngine.health_check.run_health_check',
                'schedule_type': Schedule.DAILY,
                'repeats': -1,  # infinite
            }
        )
