"""
Django settings for homeinventory project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.urls import reverse_lazy

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = environ.Path(__file__) - 3

APPS_DIR = ROOT_DIR.path('homeinventory')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables
    # defined in the .env file,
    # that is to say variables from the .env files will only be used if not
    # defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xre(ium)2hf436&-fz6fbpdqn@^r-*_8a^22mw7+g*%t#*xi+6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'widget_tweaks',
    'django_filters',
    'easy_thumbnails',
]
LOCAL_APPS = [
    'homeinventory.inventory.apps.InventoryConfig',
    'homeinventory.core.apps.CoreConfig',
    'homeinventory.accounts.apps.AccountsConfig',
    'homeinventory.dashboard.apps.DashboardConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('templates')), ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///homeinventory'),
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

PROJECT_ROOT = os.path.dirname(str(environ.Path(__file__) - 2))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
   os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[homeinventory] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # Send info messages to syslog
        # 'syslog': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.SysLogHandler',
        #     'facility': SysLogHandler.LOG_LOCAL2,
        #     'address': '/dev/log',
        #     'formatter': 'verbose',
        # },
        # Warning messages are sent to admin emails
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # critical errors are logged to sentry
        # 'sentry': {
        #     'level': 'ERROR',
        #     'filters': ['require_debug_false'],
        #     'class': 'raven.contrib.django.handlers.SentryHandler',
        # },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            # 'handlers': ['console', 'syslog', 'mail_admins', 'sentry'],
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGIN_URL = '/auth/login/'

LOGOUT_REDIRECT_URL = reverse_lazy('home')


# MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')


MEDIA_ROOT = os.path.join(os.path.dirname(
        str(environ.Path(__file__) - 2)), 'media')

MEDIA_URL = '/media/'

THUMBNAIL_ALIASES = {
    '': {
        'default': {'size': (50, 50), 'crop': True},
        'thumb100': {'size': (100, 100), 'crop': True},
    },
}

#UPGRADE DJANGO 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
