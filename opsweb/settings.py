#coding:utf8
"""
Django settings for opsweb project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '56!#5a@57c3m^r13f)=!b*jryhbu1_ug_^3eqry&6g0ew=mtcj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "dashboard",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'opsweb.urls'

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

WSGI_APPLICATION = 'opsweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': "reboot",
       'USER': 'root',
       'PASSWORD': '123456',
       'HOST': 'localhost',
       'PORT': 3306,
   },
   'tp':{
       'ENGINE': 'django.db.backends.mysql',
       'NAME': "tp",
       'USER': 'root',
       'PASSWORD': '123456',
       'HOST': 'localhost',
       'PORT': 3306,    
   }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
)

TEMPLATE_JUMP="public/jump.html"
# 无权限显示页面 跳转
PERMISSION_NONE_URL = '/permission/none/'
ZABBIX_USER='Admin'
ZABBIX_PASS='NvbzyaMXTvKq$4MU'
ZABBIX_URL='http://59.110.12.72:8000/zabbix'


LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "loggers":{
        "opsweb": {
            "level": "DEBUG",
            "handlers": ["console_handle", "opsweb_file_handle"],
            # "handlers": ["console_handle", "opsweb_file_handle",'mail'],
        },
        "django":{
            "level": "DEBUG",
            "handlers": [ "django_handle"],
        },
    },
    "handlers":{
        "console_handle": {
            "class": "logging.StreamHandler",
            "formatter": 'simple'
        },
        "opsweb_file_handle": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "opsweb.log"),
            "formatter": "opsweb"
        },
        # "mail":{
        #   "class":'logging.handlers.SMTPHandler',
        #   'level':'DEBUG',
        #   'formatter':'opsweb',
        #   'mailhost':('smtp.126.com',25),
        #   'fromaddr':'longpengcheng2006@126.com',
        #   'toaddrs':['Jiker4836@163.com'],
        #   'subject':'lpc devops mail',
        #   'credentials':('longpengcheng2006','password'),
        # },
        "django_handle":{
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "formatter": "opsweb"
        }
    },
    'formatters': {
    'opsweb':{
      'format': '%(asctime)s - %(pathname)s:%(lineno)d[%(levelname)s] - %(message)s'
    },
    'simple': {
      'format': '%(asctime)s %(levelname)s %(message)s'
    }
  },
}

LOGIN_URL="/login"