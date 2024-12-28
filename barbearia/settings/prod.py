from barbearia.settings.base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = ''

print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")