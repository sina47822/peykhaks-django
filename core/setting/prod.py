from core.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-29#q4j817$_p#ol#yp(gg=sdw21*$3qyd)6b=o#kuqzq^atzuf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['peykhaksang.com','www.peykhaksang.com']

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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'peykhaks_db',
        'USER': 'peykhaks_user1',
        'PASSWORD': 'VWx0zqW&^=MA',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = '/home/peykhaks/public_html/static'
MEDIA_ROOT = '/home/peykhaks/public_html/media'