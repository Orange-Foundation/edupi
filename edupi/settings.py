"""
Django settings for edupi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uz#38i83qtu!#f^^4f7=zs311hg)_82kd&uf4!8f2&q3i30+p#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['edupi.fondationorange.org']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'djangobower',
    'imagekit',
    # Internal apps
    'cntapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ),  # enable on prod
    'DEFAULT_PAGINATION_CLASS': 'edupi.pagination.SimpleLimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'edupi.permissions.IsAdminOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

ROOT_URLCONF = 'edupi.urls'

WSGI_APPLICATION = 'edupi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATIC_ROOT = os.path.join(BASE_DIR, "../static/")

BOWER_COMPONENTS_ROOT = os.path.abspath(os.path.join(BASE_DIR, "libs"))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "libs/bower_components"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_INSTALLED_APPS = (
    'jquery#2.1.3',
    'bootstrap#3.3.4',
    'x-editable#1.5.1',
    'bootstrap-table#1.8.0',
    'underscore#1.8.3',
    'backbone#1.1.2',
    'requirejs#2.1.17',
    'requirejs-text#2.0.14',
    'dropzone#4.0.1',
    'i18next#1.10.2',
)

MEDIA_ROOT = os.path.join(BASE_DIR, "../media/")

MEDIA_URL = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEST_RUNNER = 'edupi.runner.CustomTestSuiteRunner'

# wand can only read file from disk, so
# never keep uploaded file in memory
FILE_UPLOAD_MAX_MEMORY_SIZE = 0

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',  # use this to disable server cache
    }
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60 * 24,
    'DEFAULT_KEY_CONSTRUCTOR_MEMOIZE_FOR_REQUEST': True
}

NGINX_LOG_DIR = '/var/log/nginx/'
NGINX_MEDIA_ACCESS_LOG_PREFIX = 'edupi_media_access'
STATS_DIR = os.path.join(BASE_DIR, '../stats/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },
        'cntapp': {
            'handlers': ['console', 'logfile'],
            'level': 'WARN',
        },
    }
}
