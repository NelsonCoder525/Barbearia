from barbearia.settings.base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get("SECRET_KEY")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'barbearia.settings.prod'))

print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")