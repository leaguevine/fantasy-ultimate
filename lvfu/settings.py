# Django settings for lvfu project.
import os
import sys

import dj_database_url


# Test to see if local_settings exists. If it doesn't exist then this is on the live host.
if os.path.isfile('lvfu/local_settings.py'):
    LIVEHOST = False
else:
    LIVEHOST = True

S3_URL = 'https://s3.amazonaws.com/lvfantasyultimate/'
USE_STATICFILES = False

if LIVEHOST:
    DEBUG = False

    PROJECT_ROOT = '/app/'

    # Heroku settings: https://devcenter.heroku.com/articles/django#database-settings
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

    # Import the Facebook App ID and Facebook API secret from our heroku config
    # See here for how this works: https://devcenter.heroku.com/articles/config-vars#example
    FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID'] 
    FACEBOOK_API_SECRET = os.environ['FACEBOOK_API_SECRET']

    # Django storages
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    USE_STATICFILES = True

    # URL prefix for static files.
    STATIC_URL = S3_URL

else:
    DEBUG = True

    PROJECT_ROOT = '%s/..' % (os.path.abspath(os.path.dirname(__file__)))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'lvfu',
            'USER': 'lvfu',
            'PASSWORD': 'lvfu',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # URL prefix for static files.
    STATIC_URL = '/static/'

    # Set these in your local_settings.py file instead of here. For security
    # reasons, they should never be committed to settings.py.
    FACEBOOK_APP_ID = ''
    FACEBOOK_API_SECRET = ''

    # Django storages
    AWS_ACCESS_KEY_ID = '' # To use this to upload files to S3, this should be defined in local_settings.py
    AWS_SECRET_ACCESS_KEY = '' # To use this to upload files to S3, this should be defined in local_settings.py
    if 'collectstatic' in sys.argv:
        USE_STATICFILES = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'
TIME_ZONE = TIME_ZONE # Fix warning

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static/")
ADMIN_MEDIA_PREFIX = 'http://localhost:8000/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$wt_0m(mf$fz@p**0y5l=^$p=341p!79zl@yf_3d15prnd2m=u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'social_auth.context_processors.social_auth_by_name_backends',
    'lvfu.context_processors.facebook',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lvfu.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lvfu.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'social_auth',
    'storages',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#
# Debug toolbar
#
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#
# Are we secure by default?
#
SITE_PROTOCOL = 'http'

#
# Social auth settings
#
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/welcome'

FACEBOOK_EXTENDED_PERMISSIONS = ['email']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

CACHES = {
    'default': {
        'BACKEND': 'caching.backends.locmem.CacheClass',
    }
}

# Try to enable caching counts..for only for a short time
CACHE_COUNT_TIMEOUT = 10

# The page that users must like in order to log in
FACEBOOK_FAN_PAGE_ID = '300060247272'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Uncomment to enable console logging of all SQL queries
        #'django.db.backends': {
        #    'handlers': ['console'],
        #    'level': 'DEBUG',
        #    'propagate': True
        #},
    }
}



##############################################################################
# Django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
if USE_STATICFILES:
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_STORAGE_BUCKET_NAME = 'lvfantasyultimate'
GZIP_CONTENT_TYPES = ('text/css', 'application/javascript', 'application/x-javascript', 'text/html')
AWS_IS_GZIPPED = True
AWS_HEADERS = {
    'Cache-Control': 'max-age=3600',
}

try:
    from local_settings import *
except ImportError:
    pass
