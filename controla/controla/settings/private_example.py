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