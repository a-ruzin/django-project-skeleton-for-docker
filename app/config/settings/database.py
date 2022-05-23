import os

env = os.environ.get

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'NAME': env('POSTGRES_DB'),
    }
}
