import os
from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .auth import AUTH_PASSWORD_VALIDATORS
from .base_dirs import BASE_DIR, BIN_DIR, LOCKS_DIR, LOGS_DIR
from .database import DATABASES
from .logging import LOGGING

env = os.environ.get

DEBUG = env("DEBUG") == "True"
SECRET_KEY = env("SECRET_KEY")

PROJECT_PROTOCOL = env("PROJECT_PROTOCOL") or "http"
PROJECT_DOMAIN = env("PROJECT_DOMAIN") or "localhost"
PROJECT_PORT = env("PROJECT_PORT") or 80
PROJECT_PORT_SSL = env("PROJECT_PORT_SSL") or 443
FRONTEND_PROJECT_DOMAIN = env("FRONTEND_PROJECT_DOMAIN") or ""

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_RU = 'ru'
LANGUAGE_EN = 'en'
LANGUAGE_ES = 'es'

LANGUAGES = [(LANGUAGE_RU, 'Русский'), (LANGUAGE_EN, 'English'), (LANGUAGE_ES, 'Español')]

LANGUAGE_LIST = [LANGUAGE_RU, LANGUAGE_EN, LANGUAGE_ES]

LANGUAGE_CODE = LANGUAGE_RU
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (BASE_DIR / 'locale',)

MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_RU
MODELTRANSLATION_AUTO_POPULATE = True

# command translatemessages
TRANSLATEMESSAGES_PARAMS = {
    'source_lang': LANGUAGE_RU,
    'auto_fuzzy': False,
    'translator': {'class': 'DeeplTranslator', 'params': {'api_key': env("DEEPL_AUTH_KEY")}},
}

AUTH_USER_MODEL = "core.User"


# CSRF_COOKIE_SECURE = False
def is_port_standard(protocol: str, port: str | int) -> bool:
    if protocol == "http":
        return int(port) == 80
    else:
        return int(port) == 443


PORT_IS_STANDARD = is_port_standard(PROJECT_PROTOCOL, PROJECT_PORT)


def get_full_project_url(protocol: str, domain: str, port: str | int, port_ssl: str | int) -> str:
    if is_port_standard(protocol, port):
        full_project_url = f"{protocol}://{domain}"
    else:
        full_project_url = f"{protocol}://{domain}:{port}"
    return full_project_url


CSRF_TRUSTED_ORIGINS = [get_full_project_url(PROJECT_PROTOCOL, PROJECT_DOMAIN, PROJECT_PORT, PROJECT_PORT_SSL)]
if FRONTEND_PROJECT_DOMAIN and FRONTEND_PROJECT_DOMAIN != PROJECT_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(
        get_full_project_url(PROJECT_PROTOCOL, FRONTEND_PROJECT_DOMAIN, PROJECT_PORT, PROJECT_PORT_SSL)
    )

CSRF_TRUSTED_ORIGINS += ['http://localhost:3000']
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = '/'

ALLOWED_HOSTS = [PROJECT_DOMAIN, FRONTEND_PROJECT_DOMAIN, 'app']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = not PORT_IS_STANDARD

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rangefilter",
    "rest_framework",  # DRF
    "rest_framework_simplejwt",  # DRF
    "django_filters",  # DRF
    "drf_yasg",  # DRF
    'django_celery_results',
    "core",
    "django_translatemessages",
    "admin_auto_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Should be near the top
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session before auth
    "corsheaders.middleware.CorsMiddleware",  # CorsMiddleware should come before CommonMiddleware
    "django.middleware.common.CommonMiddleware",  # Common middlewares
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF before auth
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # After session
    "django.contrib.messages.middleware.MessageMiddleware",  # Needs sessions
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Security-related
    "django.middleware.locale.LocaleMiddleware",  # Locale typically near the end
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # WEB интерфейс для API
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # Аутентификация по JWT-токену
        # "rest_framework.authentication.SessionAuthentication",  # Стандартная (session) django аутентификация
        # "rest_framework.authentication.BasicAuthentication",  # Basic аутентификация
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPagination',
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append("rest_framework.authentication.SessionAuthentication")

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Set access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Set refresh token lifetime
    'ROTATE_REFRESH_TOKENS': False,  # Optional: Control refresh token rotation
    'BLACKLIST_AFTER_ROTATION': True,  # Optional: Blacklist old tokens after refresh
}

SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "core.api.v1.urls.api_info",
    "DEFAULT_API_URL": f'{PROJECT_PROTOCOL}://{env("PROJECT_DOMAIN")}:{env("PROJECT_PORT")}',
}


sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    server_name=f"{PROJECT_PROTOCOL}://{PROJECT_DOMAIN}:{PROJECT_PORT}",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    # traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

CELERY_BROKER_URL = f'amqp://{env("RABBITMQ_DEFAULT_USER")}:{env("RABBITMQ_DEFAULT_PASS")}@rabbit:5672'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXTENDED = True
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_IMPORTS = ('core.celery.tasks',)

PROXY = env("PROXY")
OPENAI_CONFIG = {
    'API_KEY': env("OPENAI_API_KEY"),
    'GPT_MODEL': env("OPENAI_GPT_MODEL"),
    'ASSISTANT_ID': env("OPENAI_ASSISTANT_ID"),
}

KID_URL = env("KID_URL")
KID_SECRET = env("KID_SECRET")
KID_SITE_ID = env("KID_SITE_ID")
