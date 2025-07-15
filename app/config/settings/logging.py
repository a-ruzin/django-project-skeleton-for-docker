import os
import sys

from .base_dirs import LOGS_DIR

env = os.environ.get


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
        "simple": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "default", "stream": sys.stdout},
        "command_file": {
            "level": "INFO",
            "formatter": "default",
            # https://docs.python.org/3/howto/logging-cookbook.html#customizing-handlers-with-dictconfig
            "()": "ext://lib.utils.get_command_folder_rotating_file_handler",
            "maxBytes": 100000000,
            "backupCount": 5,
            "encoding": "utf-8",
            "delay": True,
        },
        'celery_file': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}/celery.log',
            'maxBytes': 100000000,
            'backupCount': 5,
            'encoding': 'utf-8',
            # 'delay': True,
        },
        'kitglobal_file': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}/kitglobal_client.log',
            'maxBytes': 100000000,
            'backupCount': 5,
            'encoding': 'utf-8',
            # 'delay': True,
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "django.request": {"handlers": [], "level": "ERROR", "propagate": False},  # 'sentry'
        "app.command": {"handlers": ["command_file", "console"], "level": "INFO", "propagate": False},  # 'sentry'
        'celery': {'handlers': ['celery_file', 'console'], 'level': 'DEBUG', 'propagate': True},
        'kitglobal': {'handlers': ['kitglobal_file', 'console'], 'level': 'DEBUG', 'propagate': False},
        "": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
