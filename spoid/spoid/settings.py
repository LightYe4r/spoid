"""
Django settings for spoid project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
import os
import logging
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.django.middleware import XRayMiddleware

os.environ['AWS_XRAY_CONTEXT_MISSING'] = 'LOG_ERROR'
os.environ['AWS_XRAY_DAEMON_ADDRESS'] = 'xray-service.amazon-cloudwatch.svc.cluster.local:2000'
os.environ['AWS_XRAY_TRACING_NAME'] = 'My application'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# environ 초기화
env = environ.Env(DEBUG=(bool, False))

# .env 파일 로드
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'aws_xray_sdk.ext.django',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'main',
    'login',
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
    'aws_xray_sdk.ext.django.middleware.XRayMiddleware',
]

# XRAY_RECORDER = {
#     'AWS_XRAY_CONTEXT_MISSING': 'LOG_ERROR',
#     'AWS_XRAY_DAEMON_ADDRESS': 'xray-service.amazon-cloudwatch.svc.cluster.local:2000',
#     'AWS_XRAY_TRACING_NAME': 'My application',
#     'SAMPLING': False,
# }

# xray_recorder.configure(**XRAY_RECORDER)
# AWS X-Ray 설정
XRAY_RECORDER_CONFIG = {
    'AWS_XRAY_DAEMON_ADDRESS': 'xray-service.amazon-cloudwatch.svc.cluster.local:2000',  # 이 주소가 올바른지 확인
    'AWS_XRAY_TRACING_NAME': 'My application',
}

# X-Ray recorder 구성
xray_recorder.configure(service=XRAY_RECORDER_CONFIG['AWS_XRAY_TRACING_NAME'], 
                        daemon_address=XRAY_RECORDER_CONFIG['AWS_XRAY_DAEMON_ADDRESS'])
patch_all()

logger.info('X-Ray recorder configured')
logger.info(xray_recorder)
logger.info('X-Ray recorder patched')

ROOT_URLCONF = 'spoid.urls'

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

CORS_ALLOW_ALL_ORIGINS = True

WSGI_APPLICATION = 'spoid.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': env('PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AWS Cognito settings
AWS_COGNITO_REGION = env('AWS_COGNITO_REGION')
AWS_USER_POOL_ID = env('AWS_USER_POOL_ID')
AWS_COGNITO_CLIENT_ID = env('AWS_COGNITO_CLIENT_ID')
AWS_COGNITO_CLIENT_SECRET = env('AWS_COGNITO_CLIENT_SECRET')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')




