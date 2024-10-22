"""
Django settings for foodWebsite project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')

# Expected value of dev_local (sqlite3 db), dev_cloud (RDS cloud db), prod (Production with RDS Cloud db)
ENVIRONMENT = os.getenv('DJANGO_ENV', 'dev_local')  # Default to a 'dev_local' environment

if ENVIRONMENT == 'prod':
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
else:
    DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'sass_processor',
    'main.apps.MainConfig',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5'
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

ROOT_URLCONF = 'foodWebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.cart_context',
                'main.context_processors.product_stock_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodWebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# other valid values 'prod', 'dev_cloud' and 'dev_local'
if ENVIRONMENT == 'dev_local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DJANGO_DB_ENGINE'),
            'NAME': os.getenv('DJANGO_DB_NAME'),
            'USER': os.getenv('DJANGO_DB_USER'),
            'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
            'HOST': os.getenv('DJANGO_DB_HOST'),
            'PORT': os.getenv('DJANGO_DB_PORT')
        }
    }


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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "main/static/main/"),
    # Added so that auto generated css files (from sass-processor)
    # are picked up from this location. Need to see if this causes issues (looping?) as part of a prod
    # build where static files are being retrieved from the staticfiles location (after running collectstatic).
    os.path.join(BASE_DIR, "staticfiles/main/css/")
]
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'main', 'static', 'main', 'css')
SASS_PROCESSOR_ENABLED = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_SERVER_HOST = os.getenv('DJANGO_EMAIL_SERVER_HOST')
EMAIL_SERVER_PORT = os.getenv('DJANGO_EMAIL_SERVER_PORT')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL_SERVER_HOST
EMAIL_PORT = EMAIL_SERVER_PORT
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
