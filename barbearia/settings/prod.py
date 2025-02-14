from barbearia.settings.base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'barbearia.settings.prod'))



print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barbearia_db',
        'USER': 'admin',
        'PASSWORD': 'FhEWTcuajahidrEIYiaLlfYVpZabxei1',
        'HOST': 'dpg-cunp855umphs73bp9ar0-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}
