import logging

from celery import Celery

# from celery.schedules import crontab

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.beat_schedule = {'sync_every_one_hour':
# {'task': 'example_of_periodic_task', 'schedule': crontab(minute='0')}}
app.autodiscover_tasks()


def get_celery_logger() -> logging.Logger:
    """
    По какой-то причине нельзя просто написать logging.getLogger('celery') -
    у логгера не будет конфигурации, которая задана в settings.py
    """
    import logging.config

    import django.conf

    logging.config.dictConfig(django.conf.settings.LOGGING)
    logger = logging.getLogger('celery')
    return logger
