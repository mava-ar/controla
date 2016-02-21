# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "",
        'USER': "",
        'PASSWORD': "",
        "HOST": "127.0.0.1",
        "POST": "3306"
    }
}

ALLOWED_HOSTS = ['127.0.0.1', ]
import raven

RAVEN_CONFIG = {
    # 'dsn': 'https://b551e4fc1:a84f19c6d7bc2@sentry.tudominio.com.ar/1',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}
