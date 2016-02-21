from .base import *  # noqa

DEBUG = False

INSTALLED_APPS += (
    'gunicorn',
    'raven.contrib.django.raven_compat',
)

ALLOWED_HOSTS = ['127.0.0.1', ]

ADMINS = [
    ('Matias Varela', 'matias.varela@info-ingenieria.com.ar'),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': normpath(join(SITE_ROOT, '../../logs/django-debug.log')),
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_mail': {
            'handlers': ['mail_admins'],
            'propagate': True,
            'level': 'ERROR',
        },
    },
}

PIPELINE.update({'PIPELINE_ENABLED': True})
COMPRESS_ENABLED = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'Notificación <no-responder@apps.zille.com.ar>'

try:  # import the local settings
    from .private import *  # noqa
except ImportError:
    print('No tiene definidas configuraciones privadas')
