"""
* Django Project Settings
"""
# Standard Library Imports
import sys
from pathlib import Path

# Third Party Imports
from omnitils.files import load_data_file
from omnitils.logs import logger as LOGR

# Local Imports
from managarr.sources import plex as Plex

# Build paths using 'backend' directory as root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / 'env.yml'
ENV_FILE_DEFAULTS = BASE_DIR / 'env.default.yml'

# Project environment
try:
    ENV = load_data_file(ENV_FILE)
except (OSError, FileNotFoundError, ValueError):
    try:
        ENV = load_data_file(ENV_FILE_DEFAULTS)
    except Exception as e:
        LOGR.exception(e)
        LOGR.error("Couldn't initialize Django project.")
        sys.exit()

# Setup plex server connection
PlexConfig = ENV.get('PLEX', {})
PLEX_API = Plex.get_server(
    url=PlexConfig.get('HOST'),
    token=PlexConfig.get('TOKEN'),
    port=PlexConfig.get('PORT')
)

# SECURITY WARNING: Must be kept secret in production!
SECRET_KEY = ENV.get('DJANGO_SECRET', 'my-django-secret')

# SECURITY WARNING: Must be disabled in production!
DEBUG = ENV.get('DJANGO_DEBUG', False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'managarr'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Support
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ['http://localhost:*']

ROOT_URLCONF = 'managarr.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'managarr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
