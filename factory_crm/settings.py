import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / '.env'
if ENV_FILE.exists():
    for raw_line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'insecure-secret-key-change-me')
DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'crm',
    'accounts',
    'clients',
    'orders',
    'logistics',
    'reports',
    'dashboard',
    'admin_panel',
    'communications',
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
]

ROOT_URLCONF = 'factory_crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.role_flags',
                'communications.context_processors.communications_unread',
            ],
        },
    },
]

WSGI_APPLICATION = 'factory_crm.wsgi.application'
ASGI_APPLICATION = 'factory_crm.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'art_culinary_crm'),
        'USER': os.environ.get('DB_USER', 'artculinary_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    }
}

PG_DUMP_PATH = os.environ.get('PG_DUMP_PATH', 'pg_dump')
PSQL_PATH = os.environ.get('PSQL_PATH', 'psql')

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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

LOGISTICS_DEPOT_ADDRESS = os.environ.get('LOGISTICS_DEPOT_ADDRESS', 'Производство Art Culinary, Химки')
LOGISTICS_DEPOT_LAT = float(os.environ.get('LOGISTICS_DEPOT_LAT', '55.886'))
LOGISTICS_DEPOT_LNG = float(os.environ.get('LOGISTICS_DEPOT_LNG', '37.442'))
LOGISTICS_AVG_SPEED_KMH = int(os.environ.get('LOGISTICS_AVG_SPEED_KMH', '35'))
LOGISTICS_RETURN_TO_DEPOT = os.environ.get('LOGISTICS_RETURN_TO_DEPOT', 'true').lower() == 'true'
LOGISTICS_SERVICE_TIME_MINUTES = int(os.environ.get('LOGISTICS_SERVICE_TIME_MINUTES', '15'))
LOGISTICS_ALLOWED_PROOF_EXT = ['.pdf', '.jpg', '.jpeg', '.png']
LOGISTICS_MAX_PROOF_SIZE_MB = int(os.environ.get('LOGISTICS_MAX_PROOF_SIZE_MB', '10'))

ORDER_CUTOFF_TIME = "16:00"
ORDER_MORNING_CUTOFF_TIME = "10:00"
PRODUCTION_WINDOW_DAY_START = "06:00"
PRODUCTION_WINDOW_DAY_END = "18:00"
PRODUCTION_WINDOW_NIGHT_START = "22:00"
PRODUCTION_WINDOW_NIGHT_END = "06:00"
PRODUCTION_MAX_WEIGHT_KG = 500

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'crm.User'

# Email settings (configured via environment; defaults for mail.ru sender)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.mail.ru')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '465'))
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'true').lower() == 'true'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'false').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'art-culinary@mail.ru')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Z4rfpjW3dUfJPbzQebIB')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

THROTTLE_ENABLED = os.environ.get('DJANGO_THROTTLE', 'true').lower() == 'true'
if DEBUG and os.environ.get('DJANGO_THROTTLE') is None:
    THROTTLE_ENABLED = False

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    },
}

if not THROTTLE_ENABLED:
    REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
    REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Art Culinary CRM API',
    'DESCRIPTION': 'REST API для продаж, заказов, логистики и техкарт.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
}

# CORS — dev-режим (ограничьте в проде)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
