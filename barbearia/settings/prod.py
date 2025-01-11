from barbearia.settings.base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'barbearia.settings.prod'))

print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")