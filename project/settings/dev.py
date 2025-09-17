from decouple import config

from .base import *

# Configuración de desarrollo
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

# Base de datos PostgreSQL para desarrollo
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="donbosco_cup_dev"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# SECRET_KEY para desarrollo
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-dev-key-donbosco-cup-2024-change-in-production",
)

# Configuración adicional para desarrollo
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging para desarrollo
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
