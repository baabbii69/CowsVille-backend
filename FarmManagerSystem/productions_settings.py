import os

from dotenv import load_dotenv

from .settings import *

# Load environment variables
load_dotenv()

DEBUG = False
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1",
).split(",")

# Security settings for production
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() == "true"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"

# Database configuration - supports PostgreSQL (recommended)
# Support both old (DATABASE_*) and new (DB_*) variable names for compatibility

# Get database credentials - support both naming conventions
db_name = os.getenv("DB_NAME") or os.getenv("DATABASE_NAME", "farmmanager")
db_user = os.getenv("DB_USER") or os.getenv("DATABASE_USER", "farmuser")
db_password = os.getenv("DB_PASSWORD") or os.getenv(
    "DATABASE_PASSWORD", "CHANGE_ME_IN_PRODUCTION"
)
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db_name,
        "USER": db_user,
        "PASSWORD": db_password,
        "HOST": db_host,
        "PORT": db_port,
        "CONN_MAX_AGE": 60,  # Connection pooling
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CORS settings for your frontend
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000",
).split(",")

CORS_ALLOW_ALL_ORIGINS = True  # Disable in production

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Logging configuration for production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "farm_manager.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "FarmManager": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

# Disable debug toolbar in production
if "django_debug_toolbar" in INSTALLED_APPS:
    INSTALLED_APPS.remove("django_debug_toolbar")
if "debug_toolbar.middleware.DebugToolbarMiddleware" in MIDDLEWARE:
    MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")
