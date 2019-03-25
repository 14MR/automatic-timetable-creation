from celery.utils.log import get_task_logger
from atc.celery import app
logger = get_task_logger(__name__)

"""
@app.task(name="test_celery_task")
def t_celery_task():
    logger.info("test_celery_task")
    return t_celery()


def t_celery():
    c = "TEST CELERY"
    print(c)
    return c
"""