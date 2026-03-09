from celery import Task

from core.celery import app, get_celery_logger


@app.task(bind=True, name='example_of_periodic_task')
def example_of_periodic_task(self: Task) -> None:
    logger = get_celery_logger()
    logger.info('Start example_of_periodic_task', extra={'task_name': 'example_of_periodic_task', 'task': self})
