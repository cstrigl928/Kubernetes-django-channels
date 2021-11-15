# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pf-@jxtojga)z+4s*uwbgjrq$aep62-thd0q7f&o77xtpka!_m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: If you deploy a Django app to production, make sure to set
# an appropriate host here.
# See https://docs.djangoproject.com/en/1.10/ref/settings/
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'polls',
    'chatwss',
    'game',
    'gameroom',
)

import channels
print(f"Channles.version: {channels.__version__}")

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'
# Channels
ASGI_APPLICATION = 'mysite.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# [START dbconfig]
# [START gke_django_database_config]
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
print(f"DATABSE STATUS/INFO:\n\tNAME:{os.getenv('DATABASE_NAME')} \n\tUser:{os.getenv('DATABASE_USER')} \n\tPASSWORD:{os.getenv('DATABASE_PASSWORD')}")

DATABASES = {
    'default': {
        # If you are using Cloud SQL for MySQL rather than PostgreSQL, set
        # 'ENGINE': 'django.db.backends.mysql' instead of the following.
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresk8s',
        'USER': 'django_user',
        'PASSWORD': 'nach0pa$$',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
        # 'NAME': os.getenv('DATABASE_NAME'),
        # 'USER': os.getenv('DATABASE_USER'),
        # 'PASSWORD': os.getenv('DATABASE_PASSWORD'),
# Will probably want to use if we have time at the end
# [END gke_django_database_config]
# [END dbconfig]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# [START REDIS CHANNLE LAYERS]
# https://stackoverflow.com/questions/37342571/django-channels-error-cannot-import-backend-asgi-redis-redischannellayer
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
            'capacity': 1500,
            'expiry': 10,
        },
    },
}
# [END]


# Static files (CSS, JavaScript, Images)

# [START gke_django_static_config] --> Static Content (Css, JS, Media) NOw stored in Cloud
STATIC_URL = "http://storage.googleapis.com/django-k8s-331621_gameroom-static/static/"
# STATIC_URL = '/static/'
# STATIC_URL = 'https://storage.googleapis.com/[YOUR_GCS_BUCKET]/static/'
# [END gke_django_static_config]

STATIC_ROOT = 'static/'
# STATICFILES_DIRS = [ 
#     os.path.join(BASE_DIR, 'static'),
# ]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
