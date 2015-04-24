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
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'djangobower',
    # Internal apps
    'cntapp',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ),  # enable on prod
    'DEFAULT_PAGINATION_CLASS': 'edupi.pagination.SimpleLimitOffsetPagination',
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
    'bootstrap-table#1.6.0',
    'underscore#1.8.3',
    'backbone#1.1.2',
    'requirejs#2.1.17',
    'requirejs-text#2.0.14',
    'dropzone#4.0.1',
)

MEDIA_ROOT = os.path.join(BASE_DIR, "../media/")

MEDIA_URL = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEST_RUNNER = 'edupi.runner.CustomTestSuiteRunner'
