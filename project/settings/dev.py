from pathlib import Path

from .base import *

# Printeamos para ver que que variables obtuvimos
# print("clave \n", secret)

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Base de datos SQLite para desarrollo (como en donbosco_cup)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# SECRET_KEY para desarrollo
SECRET_KEY = "tu-secret-key-aqui-desarrollo-donbosco-cup-2024"
