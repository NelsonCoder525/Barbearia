from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings.dev')


app = Celery('barbearia')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task
def soma(a, b):
    # import time
    # time.sleep(5)
    return a + b