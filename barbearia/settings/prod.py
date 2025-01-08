from barbearia.settings.base import *
import os
import dj_database_url
from barbearia.settings.base import BASE_DIR

DEBUG = False
#ALLOWED_HOSTS = [os.environ.get['RENDER_EXTERNAL_HOSTNAME']]
ALLOWED_HOSTS = ['*']
#CSRF_TRUSTED_ORIGINS = ['https://'+os.environ.get['RENDER_EXTERNAL_HOSTNAME']]
SECRET_KEY = os.environ.get('SECRET_KEY')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'barbearia.settings.prod'))

print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

#CORS_ALLOWED_ORIGINS = []

STORAGES = {
    "default": {
        "BACKEND" : "django.core.files.storage.FilseSystemStorage",
    },
    "staticfiles" : {
        "BACKEND" : "whitenoise.storage.CompressedStaticFilesStorage",
    },
    
        
}


DATABASES = {
    'default': dj_database_url.config(
        #default= os.environ.get['DATABASE_URL'],
        conn_max_age=600
    )
    
    
}