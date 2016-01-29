from os.path import abspath, basename, dirname, join, normpath
from sys import path

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION

AUTH_USER_MODEL = 'users.User'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'autocomplete_light',
    'frontend',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pipeline',
    'djangobower',
    'bootstrap3',
    'compressor',
    'simple_history',

    'dj_utils',
    'modelo',
    'users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'controla.urls'

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
                "django.core.context_processors.request",
                'django.core.context_processors.media',
                'django.core.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'controla.wsgi.application'

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Mendoza'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = normpath(join(SITE_ROOT, '../media'))
STATIC_ROOT = normpath(join(SITE_ROOT, '../collected_static'))


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'pipeline.finders.PipelineFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

BOWER_COMPONENTS_ROOT = normpath(join(SITE_ROOT, '../components'))
PIPELINE_SASS_ARGUMENTS = "-p 8 -I '%s' -I '%s'" % (
         join(BOWER_COMPONENTS_ROOT, 'bower_components/bootstrap-sass/assets/stylesheets/'),
         join(BOWER_COMPONENTS_ROOT, 'bower_components/bootstrap-sass/assets/fonts/')
)

PIPELINE = {
    'PIPELINE_ENABLED': False,
    'STORAGE': STATICFILES_STORAGE,
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'bootstrap-sass/assets/stylesheets/_bootstrap.scss',
                'bootstrap3-dialog/dist/css/bootstrap-dialog.css',
                'font-awesome/css/font-awesome.min.css',
                'frontend/css/theme.bootstrap.min.css',
                'frontend/css/base.scss',
                'chosen/chosen.min.css',
            ),
            'output_filename': 'css/base.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
        # 'plugins': {
            # 'source_filenames': (
                # 'datatables/media/css/jquery.dataTables.css',
                # 'datatables/media/css/dataTables.bootstrap.css',
            # ),
            # 'output_filename': 'css/plugin.css',
        # }
    },
    'JAVASCRIPT': {
        'base_js': {
            'source_filenames': (
                'jquery/dist/jquery.js',
                'bootstrap-sass/assets/javascripts/bootstrap.js',
                'bootstrap3-dialog/dist/js/bootstrap-dialog.js',
                'chosen/chosen.jquery.min.js',
                'frontend/js/controla.js',
            ),
            'output_filename': 'js/base_js.js',
        },
        # 'plugins_js': {
            # 'source_filenames': (
                # 'datatables/media/js/jquery.dataTables.js',
                # 'datatables/media/js/dataTables.bootstrap.js',
            # ),
            # 'output_filename': 'js/plugins.js',
        # },
        'graphics_js': {
            'source_filenames': (
                "d3/d3.min.js",
                "nvd3/build/nv.d3.min.js",
                'frontend/js/graphics.js',
            ),
            'output_filename': 'js/graphics.js',
        }
    },
    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
    ),
    'SASS_BINARY': 'sassc',
    'SASS_ARGUMENTS': PIPELINE_SASS_ARGUMENTS,
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
}

# django-compressor settings
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


BOWER_INSTALLED_APPS = (
    'jquery#2.1',
    'bootstrap-sass#3.3',
    'd3#3.3.13',
    'nvd3#1.7.1',
    'fontawesome#4.5.0',
    'bootstrap3-dialog#1.34.9',
    'chosen#1.4.2'
)

ESTADO_DEFAULT = 6  # AUSENTE SIN AVISO