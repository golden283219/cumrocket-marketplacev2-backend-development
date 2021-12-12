from __future__ import absolute_import
import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplacev2.settings')
app = Celery('marketplacev2')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'task-sync-blockchain': {
        'task': 'blockchain.tasks.sync_blockchain',
        'schedule': timedelta(minutes=1),
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))