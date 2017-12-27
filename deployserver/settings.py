"""
Django settings for deployserver project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from django.urls import reverse_lazy
from config import Config as CONFIG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.SECRET_KEY


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG or False

ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS or []

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'captcha',
    'users',
    'common',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTH_USER_MODEL = 'users.User'
ROOT_URLCONF = 'deployserver.urls'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'deployserver.urls'
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('users:login')

SESSION_COOKIE_DOMAIN = CONFIG.SESSION_COOKIE_DOMAIN or None
CSRF_COOKIE_DOMAIN =  CONFIG.CSRF_COOKIE_DOMAIN or None
SESSION_COOKIE_AGE = CONFIG.SESSION_COOKIE_AGE or 60*30
SESSION_SAVE_EVERY_REQUEST = CONFIG.SESSION_SAVE_EVERY_REQUEST or True
SESSION_EXPIRE_AT_BROWSER_CLOSE = CONFIG.SESSION_EXPIRE_AT_BROWSER_CLOSE or True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'deployserver.wsgi.application'
CAPTCHA_IMAGE_SIZE = (80, 33)
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_TEST_MODE = CONFIG.CAPTCHA_TEST_MODE or False

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.%s' % CONFIG.DB_ENGINE,
        'NAME': CONFIG.DB_NAME,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.DB_PASSWORD,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
   }
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Email config
EMAIL_HOST = CONFIG.EMAIL_HOST
EMAIL_PORT = CONFIG.EMAIL_PORT
EMAIL_HOST_USER = CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = CONFIG.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = CONFIG.EMAIL_USE_SSL
EMAIL_USE_TLS = CONFIG.EMAIL_USE_TLS
EMAIL_SUBJECT_PREFIX = CONFIG.EMAIL_SUBJECT_PREFIX

# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/4' % {
            'password': CONFIG.REDIS_PASSWORD if CONFIG.REDIS_PASSWORD else '',
            'host': CONFIG.REDIS_HOST or '127.0.0.1',
            'port': CONFIG.REDIS_PORT or 6379,
        }
    }
}

# Celery using redis as broker
BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/3' % {
    'password': CONFIG.REDIS_PASSWORD if CONFIG.REDIS_PASSWORD else '',
    'host': CONFIG.REDIS_HOST or '127.0.0.1',
    'port': CONFIG.REDIS_PORT or 6379,
}
CELERY_RESULT_BACKEND = BROKER_URL