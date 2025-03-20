from barbearia.settings.base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'barbearia.settings.prod'))



print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barbearia_db_kltq',
        'USER': 'admin',
        'PASSWORD': '741fObMI5cBbXGieoSF3zKuE7uZksHt3',
        'HOST': 'dpg-cve5t9hu0jms73bd1560-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'

CELERY_BROKER_URL = os.getenv("REDIS_URL", 'redis://default:IR17pFpUUeCCkAmEdmV4IqLnIgjK1zKy@redis-13883.c336.samerica-east1-1.gce.redns.redis-cloud.com:13883')
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", 'redis://default:IR17pFpUUeCCkAmEdmV4IqLnIgjK1zKy@redis-13883.c336.samerica-east1-1.gce.redns.redis-cloud.com:13883')