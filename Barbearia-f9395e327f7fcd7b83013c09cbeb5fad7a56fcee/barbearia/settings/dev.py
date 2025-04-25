from barbearia.settings.base import *
import os

print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'django-insecure-&_bd@!)ct_w6)ej#@_6+c)n&^0*7o5(8#qn0=&hls!766r7la6'

LOGGING = {
    **LOGGING,
    'loggers': {
        '': {  # '' representa o logger "raíz" (root). Todos "loggers" herdarão dele.
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}