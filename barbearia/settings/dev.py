from barbearia.settings.base import *
import os

print(f"DjjjjjJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")

DEBUG = True
ALLOWED_HOSTS = ['*']

LOGGING = {
    **LOGGING,
    'loggers': {
        '': {  # '' representa o logger "raíz" (root). Todos "loggers" herdarão dele.
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}