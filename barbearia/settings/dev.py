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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'