# encode: utf-8
import sys

from decouple import config
from dj_database_url import parse as db_url
from unipath import Path

PROJECT_DIR = Path(__file__).parent

ADMINS = (('Thiago Garcia', 'thiagogds14@gmail.com'),)

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

TESTING = 'test' in sys.argv

ALLOWED_HOSTS = ['104.131.127.200', 'localhost', '127.0.0.1', '.ingressosgratis.com']

AUTH_USER_MODEL = 'registration.User'
LOGIN_URL = '/login/'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_email_confirmation',
    'djrill',
    'registration',
    'scrapper',
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
)

ROOT_URLCONF = 'vivo_scrapper.urls'

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

WSGI_APPLICATION = 'vivo_scrapper.wsgi.application'


DATABASES = {
        'default': config(
            'DATABASE_URL',
            default='sqlite:///' + PROJECT_DIR.child('db.sqlite3'),
            cast=db_url),
}

EMAIL_BACKEND = config('EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend'
)
DEFAULT_FROM_EMAIL = "no-reply@ingressosgratis.com"
EMAIL_HOST = 'smtp.sparkpostmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'SMTP_Injection'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = PROJECT_DIR.child('static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'stderr': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'normal',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['stderr'],
            'level': 'DEBUG',
        },
    },
}
