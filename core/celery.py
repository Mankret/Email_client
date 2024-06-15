import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'debug-task-every-20-seconds': {
        'task': 'email_client.task.debug_task_test',
        'schedule': 20.0,
    },
}


@app.task
def debug_task():
    print('Celery worked!')
