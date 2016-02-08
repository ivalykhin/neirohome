# -*- coding: utf-8 -*-
"""
Django settings for neirohome project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Environmet settings
if 'OPENSHIFT_GEAR_NAME' in os.environ:
    DB_NAME = os.environ['OPENSHIFT_GEAR_NAME']
    DB_HOST = os.environ['OPENSHIFT_MYSQL_DB_HOST']
    DB_USER = os.environ['OPENSHIFT_MYSQL_DB_USERNAME']
    DB_PASSWORD = os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']
    DB_PORT = os.environ['OPENSHIFT_MYSQL_DB_PORT']
    DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']
    NEIRONET_STORAGE = os.environ['OPENSHIFT_DATA_DIR'] + '/neironet_storage/'
else:
    DB_NAME = 'neirohome'
    DB_HOST = '127.0.0.1'
    DB_USER = 'appsuser'
    DB_PASSWORD = '1qaz&UJM'
    DB_PORT = '3306'
    NEIRONET_STORAGE = 'D:/studing/django/openshift/neironet_storage/'
    DATA_DIR = 'D:/studing/django/openshift/'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'koe=x_l56zo8$cy5&rx%cky^#=406gz2nw5ko=u5r%f22ob)p*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'djkombu',
    'prediction_research',
    'tz_detect',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'neirohome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'neirohome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'DEFAULT-CHARACTER-SET': 'utf8'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = None

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# адрес redis сервера
#BROKER_URL = 'redis://localhost:6379/0'
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
# храним результаты выполнения задач так же в redis
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# в течение какого срока храним результаты, после чего они удаляются
CELERY_TASK_RESULT_EXPIRES = 7*86400  # 7 days
# это нужно для мониторинга наших воркеров
CELERY_SEND_EVENTS = True
# место хранения периодических задач (данные для планировщика)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER=False

import djcelery
djcelery.setup_loader()