# Create your tests here.

from schedule.tasks import t_celery_task


def test_celery():
    t_celery_task.delay()
