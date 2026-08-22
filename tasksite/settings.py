"""Development settings for the TaskSwap SQLite application."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Replace this key with a private value before any public deployment.
SECRET_KEY = "django-insecure-change-this-taskswap-development-key"
DEBUG = True
# Accept local development and the sandbox preview subdomains used for browser checks.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".manus.computer"]
# POST requests from the managed HTTPS preview must pass Django's strict origin check.
CSRF_TRUSTED_ORIGINS = ["https://*.manus.computer"]
# The preview is embedded on a different secure site origin, so cookies must be sent
# with the iframe request. Set TASKSWAP_INSECURE_COOKIES=1 for plain-HTTP localhost use.
_secure_preview_cookies = os.environ.get("TASKSWAP_INSECURE_COOKIES") != "1"
CSRF_COOKIE_SECURE = _secure_preview_cookies
CSRF_COOKIE_SAMESITE = "None" if _secure_preview_cookies else "Lax"
SESSION_COOKIE_SECURE = _secure_preview_cookies
SESSION_COOKIE_SAMESITE = "None" if _secure_preview_cookies else "Lax"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tasksite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tasksite.wsgi.application"
ASGI_APPLICATION = "tasksite.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# This project deliberately uses a custom email-address login model from its first migration.
AUTH_USER_MODEL = "core.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "home"
