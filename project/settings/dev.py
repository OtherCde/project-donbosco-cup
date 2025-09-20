from decouple import config

from .base import *

# Configuración de desarrollo
# DEBUG ya se lee desde base.py, pero podemos sobrescribir si es necesario
# DEBUG = config("DEBUG", default=True, cast=bool)

# ALLOWED_HOSTS ya se lee desde base.py
# ALLOWED_HOSTS ya está configurado en base.py desde el .env

# Base de datos PostgreSQL para desarrollo
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

# SECRET_KEY para desarrollo - ya se lee desde base.py
# SECRET_KEY ya está configurado en base.py desde el .env

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
