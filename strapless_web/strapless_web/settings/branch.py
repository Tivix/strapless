from __future__ import absolute_import
import os

from .base import *


# Staging overrides
DEBUG = True
IS_STAGING = True

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# domains/hosts etc.
TLD_NAME = os.environ.get('DJANGO_TLD_NAME', '%s.com' % PROJECT_NAME)
DOMAIN_NAME = os.environ.get('DJANGO_ALLOWED_HOST', 'branch.%s' % TLD_NAME)

# Django 1.5 requirement
ALLOWED_HOSTS = [DOMAIN_NAME]

WWW_ROOT = 'http://%s/' % DOMAIN_NAME
DEFAULT_FROM_EMAIL = 'no-reply@%s' % TLD_NAME

DATABASES['default']['HOST'] = os.environ.get('DJANGO_DATABASE_URL', 'localhost')
DATABASES['default']['PORT'] = 5432

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 86400
    }
}

LOGS_PATH = os.path.join(VIRTUAL_ENV_DIR, 'logs/')
