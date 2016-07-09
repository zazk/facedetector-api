from .base import *

DEBUG = False
PREPEND_WWW = False

# DIRS

MEDIA_ROOT = ENV.get('MEDIA_ROOT', '')
MEDIA_URL = ENV.get('MEDIA_URL', '')

STATIC_ROOT = ENV.get('STATIC_ROOT', '')
STATIC_URL = ENV.get('STATIC_URL', '')
ALLOWED_HOSTS = ENV.get('ALLOWED_HOSTS', '')

# SESSIONS

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': '300',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV.get('DB_NAME'),
        'USER': ENV.get('DB_USER'),
        'PASSWORD': ENV.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

