"""
Django settings for rtaa_gis project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.urls import reverse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition
ROOT_URLCONF = r'rtaa_gis.urls'
LOGIN_URL = r'login/'
LOGIN_REDIRECT_URL = r'/'

FCGI_DEBUG = True
FCGI_LOG = True
FCGI_LOG_PATH = os.path.join(BASE_DIR, "logs")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "aspmx.l.google.com"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bo0*s)^co9abj49*kpp(+91&98v25=0s3#3bv-3-l(2hg9q!5c'
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ["localhost", "127.0.0.1", "gisapps.aroraengineers.com"]
CSRF_COOKIE_SECURE = False
CORS_REPLACE_HTTPS_REFERER = False
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'content-range',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
)

CORS_EXPOSE_HEADERS = (
    'x-requested-with',
    'content-type',
    'content-range',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
)

ALLOWED_HOSTS = [
    'gisapps.aroraengineers.com',
    'localhost',
    '127.0.0.1'
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CORS_REPLACE_HTTPS_REFERER = True
    CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework_swagger',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'fileApp.apps.FileAppConfig',
    'home.apps.HomeConfig'
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.PersistentRemoteUserMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'rtaa_gis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    # 'azure_sql_server': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'NAME': 'eDocDiscovery',
    #     'HOST': 'sql-server-azure.database.windows.net',
    #     'USER': 'gissetup@sql-server-azure',
    #     'PASSWORD': "Heddie01!",
    #     'OPTIONS': {
    #         'driver': 'SQL Server Native Client 11.0'
    #      }
    #  },
    # 'postGres': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'rtaa_DRF',
    #     'USER': 'postgres',
    #     'PASSWORD': 'AroraGIS123',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432'
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 15,
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.OrderingFilter',
        # 'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    )
}

LOGGING = {
    # TODO - setup the email logging for running on IIS
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': "DEBUG",
            'filename': os.path.join(BASE_DIR, 'logs/django_log.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter': 'standard'
        }
    },
    'loggers': {
        'fileApp': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propogate': True
        },
        'home': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propogate': True
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True