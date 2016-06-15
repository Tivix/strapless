from __future__ import absolute_import
import os, sys


####
# Change per project
####
PROJECT_NAME = 'strapless_web'
VIRTUAL_ENV_DIR = '/home/ubuntu/webapps/strapless_web'

####
# Other settings
####
ADMINS = (
    # ('Alerts', 'dev@strapless_web.com'),
    ('Alerts', 'dev@tivix.com'),
)
SITE_ID = 1
TIME_ZONE = 'America/Los_Angeles'  # changed to UTC
LANGUAGE_CODE = 'en-us'
USE_I18N = True
SECRET_KEY = 'kr43fm2^k7*h0l@bpmw#%@y6gbo8c+h6kaxm+#d)+w-_nx%8_x'
DEFAULT_CHARSET = 'utf-8'
ROOT_URLCONF = 'strapless_web.urls'

# project root and add "apps" to the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(PROJECT_ROOT, 'apps/'))

UPLOADS_DIR_NAME = 'uploads'
MEDIA_URL = '/%s/' % UPLOADS_DIR_NAME
MEDIA_ROOT = os.path.join(VIRTUAL_ENV_DIR, '%s' % UPLOADS_DIR_NAME)
FILE_UPLOAD_MAX_MEMORY_SIZE = 4194304  # 4mb


# static resources related. See documentation at: http://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/
STATIC_URL = '/static/'
STATIC_ROOT = '%s/staticserve' % VIRTUAL_ENV_DIR
STATICFILES_DIRS = (
    ('global', '%s/static' % PROJECT_ROOT),
)

# static serving
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",

    # other finders..
    "compressor.finders.CompressorFinder",
)

DEBUG = False
IS_DEV = False
IS_STAGING = False
IS_PROD = False

# Get the ENV setting. Needs to be set in .bashrc or similar.
ENV = os.getenv('ENV')
if not ENV:
    raise Exception('Environment variable ENV is required!')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%s' % PROJECT_NAME,
        'USER': '%s' % PROJECT_NAME,
        'PASSWORD': '%s!rules' % PROJECT_NAME,
        'HOST': 'localhost',
        'ATOMIC_REQUESTS': True,
    }
}

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'userswitch.middleware.UserSwitchMiddleware',

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.media',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
                'django_common.context_processors.common_settings',
                'django.template.context_processors.request',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'compressor',
    'django_common',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'marketing',
    'accounts',
    'common',
]



# Email settings #
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
# EMAIL_HOST_USER = 'dev@strapless_web.com'
# EMAIL_HOST_PASSWORD = 'TBD-strapless_web'
EMAIL_HOST_USER = 'sumit@tivix.com'
EMAIL_HOST_PASSWORD = 'Tivix!rules1!@#!'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@strapless_web.com'
EMAIL_SUBJECT_PREFIX = '[%s %s] ' % (PROJECT_NAME, ENV)


# auth / django-registration params
AUTH_USER_MODEL = 'accounts.User'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/accounts/login/error/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'PASSWORD': '', 'USER': ''}

COMPRESS_PRECOMPILERS = (
   ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_CSS_FILTERS = [
    #css minimizer
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

USERSWITCH_OPTIONS = {
    'auth_backend': 'django.contrib.auth.backends.ModelBackend',
    'css_inline': 'position:fixed !important; bottom: 10px !important; left: 10px !important; opacity:0.50; z-index: 9999;',
}

# helper function to extend all the common lists
def extend_list_avoid_repeats(list_to_extend, extend_with):
    """Extends the first list with the elements in the second one, making sure its elements are not already there in the
    original list."""
    list_to_extend.extend(filter(lambda x: not list_to_extend.count(x), extend_with))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s line %(lineno)d: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'common.utils.DeferredRotatingFileHandler',
            'filename': 'django.log',  # Full path is created by DeferredRotatingFileHandler.
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True},
        'django.request': {
            'handlers': ['mail_admins', 'default'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            # Skip "SuspiciousOperation: Invalid HTTP_HOST" e-mails.
            'handlers': ['default'],
            'propagate': False,
        },
    }
}

# see http://django-allauth.readthedocs.org/en/latest/configuration.html for
# more config options
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.SignupForm'
}
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_ADAPTER = 'accounts.adapter.DefaultAccountAdapter'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# Determines the e-mail verification method during signup -
# choose one of "mandatory", "optional", or "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
