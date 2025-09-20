from decouple import config

from .base import *

# Configuración de producción
# DEBUG ya se lee desde base.py, pero podemos sobrescribir si es necesario
# DEBUG = config("DEBUG", default=False, cast=bool)

# Las siguientes variables ya se leen desde base.py desde el .env:
# ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, CORS_ALLOWED_ORIGINS
# SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, SECURE_SSL_REDIRECT

# Redirección a HTTPS detrás de proxy/Nginx
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Base de datos PostgreSQL para producción
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# SECRET_KEY para producción - ya se lee desde base.py
# SECRET_KEY ya está configurado en base.py desde el .env

# Configuración de seguridad adicional
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"

# Configuración de email para producción
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="")

# Logging para producción
import os

# Crear directorio de logs si no existe
LOG_DIR = config("LOG_DIR", default="/var/log/django")
LOG_FILE = config("LOG_FILE", default="donbosco_cup.log")

# Configuración flexible de logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Agregar handler de archivo solo si el directorio existe o se puede crear
try:
    os.makedirs(LOG_DIR, exist_ok=True)
    LOGGING["handlers"]["file"] = {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": os.path.join(LOG_DIR, LOG_FILE),
        "formatter": "verbose",
    }
    LOGGING["root"]["handlers"].append("file")
except (OSError, PermissionError):
    # Si no se puede crear el directorio o archivo, solo usar console
    pass
