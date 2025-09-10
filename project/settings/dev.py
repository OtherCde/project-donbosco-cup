from .base import *
from pathlib import Path

# Printeamos para ver que que variables obtuvimos
#print("clave \n", secret)

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de datos SQLite para desarrollo (como en donbosco_cup)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Usar SECRET_KEY por defecto si no está en .env
try:
    SECRET_KEY = env('SECRET_KEY')
except:
    SECRET_KEY = 'tu-secret-key-aqui-desarrollo'