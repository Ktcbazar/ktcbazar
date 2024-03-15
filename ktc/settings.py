from pathlib import Path
import sys
import os
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=j4a=yxmqg-$jg*6wuugio8lqq$)=$p#(ftgs@ox7o-7#ns1qk'

if (len(sys.argv) >= 2 and sys.argv[1] == 'runserver'):
    DEBUG = True
else:
    DEBUG = False
    

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bazar',
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

ROOT_URLCONF = 'ktc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bazar/templates/forntend'),
                 os.path.join(BASE_DIR, 'bazar/templates/registration'),
                 os.path.join(BASE_DIR, 'bazar/templates/dashboard'),
                 os.path.join(BASE_DIR, 'bazar/templates/customer_profile'),
                 os.path.join(BASE_DIR, 'bazar/templates/agent_profile'),
                 os.path.join(BASE_DIR, 'bazar/templates/staff_profile'),
                 os.path.join(BASE_DIR, 'bazar/templates/employee_profile'),
                 os.path.join(BASE_DIR, 'bazar/templates/data_input'),
                 os.path.join(BASE_DIR, 'bazar/templates/tree'),
                 os.path.join(BASE_DIR, 'bazar/templates/supplier'),
                 os.path.join(BASE_DIR, 'bazar/templates/product_category'),
                 os.path.join(BASE_DIR, 'bazar/templates/product'),
                 os.path.join(BASE_DIR, 'bazar/templates/shop'),
                 os.path.join(BASE_DIR, 'bazar/templates/commission'),
                 os.path.join(BASE_DIR, 'bazar/templates/send_money'),
                 os.path.join(BASE_DIR, 'bazar/templates/withdrawal'),
                 os.path.join(BASE_DIR, 'bazar/templates/agent_withdrawal'),
                 os.path.join(BASE_DIR, 'bazar/templates/password'),],
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


WSGI_APPLICATION = 'ktc.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecomapp',
        'USER': 'tomal',  
        'PASSWORD': 'tomal1234',  
        'HOST': 'localhost',  
        'PORT': '3306',  
    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'bazar/static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'bazar.CustomUser'

LOGIN_URL = 'login'


BASE_URL = 'http://127.0.0.1:8000/'


#Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ftextrading@gmail.com'
EMAIL_HOST_PASSWORD = 'kqrovkgeaghpwluo'
DEFAULT_FROM_EMAIL = 'ftextrading@gmail.com'