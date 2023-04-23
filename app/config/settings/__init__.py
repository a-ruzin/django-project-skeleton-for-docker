import os
from pathlib import Path

from .database import DATABASES
from .auth import AUTH_PASSWORD_VALIDATORS
from .logging import LOGGING

env = os.environ.get

DEBUG = env('DEBUG') == "True"
SECRET_KEY = env('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / 'logs'
LOCKS_DIR = BASE_DIR / 'locks'

PROJECT_PROTOCOL = env('PROJECT_PROTOCOL') or 'http'
PROJECT_DOMAIN = env('PROJECT_DOMAIN') or 'localhost'
PROJECT_PORT = env('PROJECT_PORT') or 80
PROJECT_PORT_SSL = env('PROJECT_PORT_SSL') or 443

ALLOWED_HOSTS = env('ALLOWED_HOSTS', '').split(' ')
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = 'core.User'

# CSRF_COOKIE_SECURE = False
if PROJECT_PROTOCOL == 'http':
    if int(PROJECT_PORT) == 80:
        CSRF_TRUSTED_ORIGINS = [f'{PROJECT_PROTOCOL}://{PROJECT_DOMAIN}']
    else:
        CSRF_TRUSTED_ORIGINS = [f'{PROJECT_PROTOCOL}://{PROJECT_DOMAIN}:{PROJECT_PORT}']
else:
    if int(PROJECT_PORT_SSL) == 443:
        CSRF_TRUSTED_ORIGINS = [f'{PROJECT_PROTOCOL}://{PROJECT_DOMAIN}']
    else:
        CSRF_TRUSTED_ORIGINS = [f'{PROJECT_PROTOCOL}://{PROJECT_DOMAIN}:{PROJECT_PORT_SSL}']

# AUTH_USER_MODEL = 'main.User'
# LOGIN_URL = "main:auth_login"


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
