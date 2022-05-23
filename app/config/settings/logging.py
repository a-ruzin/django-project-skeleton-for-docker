import os
import sys

env = os.environ.get


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        # 'sentry': {
        #     'level': 'ERROR',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout
        },
        "command_file": {
            'level': 'INFO',
            'formatter': 'default',
            # https://docs.python.org/3/howto/logging-cookbook.html#customizing-handlers-with-dictconfig
            '()': 'ext://lib.utils.get_command_folder_rotating_file_handler',
            'maxBytes': 100000000,
            'backupCount': 5,
            'encoding': 'utf-8',
            'delay': True,
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': [],  # 'sentry'
            'level': 'ERROR',
            'propagate': False,
        },
        "app.command": {
            'handlers': ['command_file', 'console'],  # 'sentry'
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
