from .base import *

# Printeamos para ver que que variables obtuvimos
#print("clave \n", secret)

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Actualizar con el dominio real del proyecto

# Orígenes confiables para CSRF
CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
]

# CORS: permitir sólo el frontend
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Cookies seguras en producción
SESSION_COOKIE_SECURE = False  # Cambiar a True cuando se use HTTPS
CSRF_COOKIE_SECURE = False     # Cambiar a True cuando se use HTTPS

# Redirección a HTTPS detrás de proxy/Nginx
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Base de datos SQLite para producción (cambiar a PostgreSQL cuando sea necesario)
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
    SECRET_KEY = 'tu-secret-key-aqui-produccion'
