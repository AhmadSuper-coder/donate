"""
Django settings for donate project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from decouple import config
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-juz$z8fck3ks6^4cmw2xqlv(%qs$lgk9^61_p=$870!n!jtau3'
SECRET_KEY = config('SECRET_KEY', default='your_default_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['rankuptechnology.pythonanywhere.com', "pay.angelsfoundationindia.org", "*"]


CSRF_TRUSTED_ORIGINS = [
    'https://pay.angelsfoundationindia.org', 
    'https://www.pay.angelsfoundationindia.org'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #restframeworks
    "rest_framework",

    # Custom apps
    'backend_apps.central',
    'backend_apps.donate_once',
    'backend_apps.subscription',
    "templates_app"
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'donate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Set the template directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'donate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# mysql, postgresql

# for the postgres sql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME', default='donate_db'),
        'USER': config('DATABASE_USER', default='donate_user'),
        'PASSWORD': config('DATABASE_PASSWORD', default='your_secure_password'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

# print("DATABASE_NAME:", config('DATABASE_NAME', default='donate_db'))
# print("DATABASE_USER:", config('DATABASE_USER', default='donate_user'))
# print("DATABASE_PASSWORD:", config('DATABASE_PASSWORD', default='your_secure_password'))
# print("DATABASE_HOST:", config('DATABASE_HOST', default='localhost'))
# print("DATABASE_PORT:", config('DATABASE_PORT', default='5432'))
# print("SECRET_KEY:", config('SECRET_KEY', default='your_default_secret_key'))


# PhonePe related credentials
PHONEPE_TESTING_MERCHANT_ID = config('TESTING_MERCHANT_ID', default='default_testing_merchant_id')
PHONEPE_TESTING_SALTKEY = config('TESTING_SALTKEY', default='default_testing_saltkey')
PHONEPE_TESTING_SALTINDEX = config('TESTING_SALTINDEX', default='default_testing_saltindex')
PHONEPE_TESTING_URL = config('TESTING_PHONPE_URL', default='https://test.phonepe.com/api')

PHONEPE_PROD_MERCHANT_ID = config('PROD_MERCHANT_ID', default='default_prod_merchant_id')
PHONEPE_PROD_SALTKEY = config('PROD_SALTKEY', default='default_prod_saltkey')
PHONEPE_PROD_SALTINDEX = config('PROD_SALTINDEX', default='default_prod_saltindex')
PHONEPE_PROD_URL = config('PROD_PHONPE_URL', default='https://prod.phonepe.com/api')


# this will enabkle the testing thing here 
PHONEPE_ENV="TESTING"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Tells Django to look for static files here
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Change if needed


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
