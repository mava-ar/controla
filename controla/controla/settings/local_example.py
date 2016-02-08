from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '123123123'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "controla",
        'USER': "",
        'PASSWORD': "",
        "HOST": "127.0.0.1",
        "POST": "3306"
    }
}

COMPRESS_ENABLED = False

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': 'http://127.0.0.1:8000/static/jquery/dist/jquery.js',
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''