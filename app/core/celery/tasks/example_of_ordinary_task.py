from celery import Task

from core.celery import app, get_celery_logger


@app.task(bind=True, name='example_of_ordinary_task')
def example_of_ordinary_task(self: Task, project_id: int) -> None:
    logger = get_celery_logger()
    logger.info('Start example_of_ordinary_task', extra={'task_name': 'example_of_ordinary_task', 'task': self})
