
from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*puu1h89t-w(e(1l7ljoqblrpf@e@+6a-f&hz(55ttwl2#@o-k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_q',
    'corsheaders',
    'executor',
    'django_cron',
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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
ROOT_URLCONF = 'nessusEngine.urls'

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

WSGI_APPLICATION = 'nessusEngine.wsgi.application'

CRON_CLASSES = [
    "executor.nessus_cronjob.PerformScan", # Helps to check progress of Nessus scan
]

Q_CLUSTER = {
    'name': 'nessus',
    'workers': 1,
    'recycle': 500,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    # 'ack_failures': True,
    # 'attempt_count': 1,
    'redis': {
        # 'host': 'host.docker.internal', //if redis runs on different server
        'host' : 'redis',
        'password': env("REDIS_PASSWORD", default=None),
        'port': 6379,
        'db': 0, 
    }
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nessus_db',
        'USER': 'root',
        'PASSWORD': 'test1234',
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# AWS credentials for boto3
AWS_ACCESS_KEY = env('AWS_ACCESS_KEY',default='')
AWS_SECRET_KEY = env('AWS_SECRET_KEY',default='')

S3_BUCKET_REGION = env('S3_BUCKET_REGION')
S3_BUCKET_NAME = env('S3_BUCKET_NAME')

NESSUS_USERNAME = env('NESSUS_USERNAME')
NESSUS_PWD = env('NESSUS_PWD')
SERVER_HOST = env('SERVER_HOST')
SERVER_PORT = env('SERVER_PORT')
NESSUS_ACCESS_KEY = env('NESSUS_ACCESS_KEY', default="")
NESSUS_SECRET_KEY = env('NESSUS_SECRET_KEY', default="")
CORE_URL = env('CORE_URL',default='http://3.29.96.110/api/')
JWT_SERVICE_SECRET = env('JWT_SERVICE_SECRET', default='')