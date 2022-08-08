"""
Django settings for backend project.

Generated by "django-admin startproject" using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv("DJANGO_DEBUG", 'False').lower() in ('true', '1', 't')

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
if not DEBUG and not SECRET_KEY:
    raise Exception("DJANGO_SECRET_KEY environment variable is not set")

# ALLOWED_HOSTS = ["localhost:8001", "127.0.0.1:8001"]  # doesn't work
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8001", "http://127.0.0.1:8001"]

# ALLOWED_HOSTS = ["whataretheodds.com", "www.whataretheodds.com"]
# CSRF_TRUSTED_ORIGINS = ["https://whataretheodds.com", "https://www.whataretheodds.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # TODO pip-autoremove django-cors-headers

    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    # "drf_spectacular",

    # Local apps
    "core",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"  # TODO ?

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "whataretheodds"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# path of static files in url
# path of static files in filesystem
# extra static files

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "frontend/build/static")]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    # "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# SPECTACULAR_SETTINGS = {
#     'TITLE': 'Your Project API',
#     'DESCRIPTION': 'Your project description',
#     'VERSION': '1.0.0',
#     'SERVE_INCLUDE_SCHEMA': False,
#     # OTHER SETTINGS
# }

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AUTH_USER_MODEL = "core.UserAccount"

CRONJOBS = [  # TODO replace with celery beat
    ("0 0 * * *", "core.cron.track_price_history"),
]

CELERY_BROKER_URL = "redis://" + os.getenv("REDIS_HOST", "redis") + ":" + os.getenv("REDIS_PORT", "6379")
