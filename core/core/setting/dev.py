from core.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-29#q4j817$_p#ol#yp(gg=sdw21*$3qyd)6b=o#kuqzq^atzuf'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = ['5.34.205.103']

SECRET_KEY = config("SECRET_KEY", default="test")
DEBUG = config("DEBUG", cast=bool, default=True)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="*",
)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'peykhaks_db',
#         'USER': 'peykhaks_user1',
#         'PASSWORD': 'VWx0zqW&^=MA',
#         'HOST': 'localhost',
#         'PORT': 3306,
#     }
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]