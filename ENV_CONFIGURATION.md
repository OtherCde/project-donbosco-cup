# 🔧 Configuración de Variables de Entorno

## 📋 Cómo Ver y Usar el .env Generado en GitHub Actions

### **Método 1: Ver en los Logs del Workflow**

1. **Ejecutar el workflow "🔧 Generate Production .env"**:
   - Ve a **Actions** en tu repositorio
   - Selecciona **"🔧 Generate Production .env"**
   - Haz clic en **"Run workflow"**
   - Elige el entorno (development/staging/production)

2. **Ver el contenido en los logs**:
   - El workflow mostrará el contenido completo del `.env`
   - Las passwords estarán ocultas por seguridad
   - Verás todas las variables configuradas para el entorno

### **Método 2: Descargar como Artifact**

1. **Después de ejecutar el workflow**:
   - Ve a la sección **Artifacts** del workflow ejecutado
   - Descarga `env-file-[environment]`
   - Renómbralo a `.env` en tu servidor

### **Método 3: Usar el Workflow de Setup Environment**

1. **Ejecutar "🔧 Setup Environment"**:
   - Muestra configuración en tiempo real
   - Guarda el `.env` como artifact
   - Incluye verificación completa del entorno

## 🔐 Variables que Necesitas Configurar Manualmente

### **Variables Críticas (OBLIGATORIAS):**

```bash
# Django
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura

# Base de datos
DB_PASSWORD=tu-password-de-base-de-datos

# Hosts permitidos (para producción)
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

### **Variables Opcionales:**

```bash
# Email (si usas servicio de email)
EMAIL_HOST_PASSWORD=tu-password-del-servicio-email

# Logging
LOG_DIR=/var/log/django
LOG_FILE=donbosco_cup.log
```

## 🚀 Configuración para Producción

### **1. Generar .env para Producción:**

```bash
# Ejecutar workflow "Generate Production .env" con environment=production
# Descargar el artifact generado
```

### **2. Configurar Variables Sensibles:**

```bash
# Editar el .env descargado
nano .env

# Configurar variables críticas:
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DB_PASSWORD=tu-password-super-seguro
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

### **3. Subir a tu Servidor:**

```bash
# Copiar al servidor
scp .env usuario@tu-servidor:/ruta/del/proyecto/

# Verificar permisos
chmod 600 .env
```

## 📊 Ejemplo de .env para Producción

```bash
# Django Settings
SECRET_KEY=django-insecure-cambiar-por-una-clave-real
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Database Settings (PostgreSQL)
DB_NAME=donbosco_cup_prod
DB_USER=postgres
DB_PASSWORD=***CONFIGURAR***
DB_HOST=localhost
DB_PORT=5432

# Security Settings
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# CORS Settings
CORS_ALLOWED_ORIGINS=https://tu-frontend.com
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com

# Email Settings (opcional)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=***CONFIGURAR***
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com

# Logging
LOG_DIR=/var/log/django
LOG_FILE=donbosco_cup.log
```

## 🔍 Verificar Configuración

### **Comandos de Verificación:**

```bash
# Verificar que Django puede cargar la configuración
python manage.py check --settings=project.settings.prod

# Verificar variables de entorno
python -c "from decouple import config; print('DB_NAME:', config('DB_NAME'))"

# Verificar conexión a base de datos
python manage.py dbshell --settings=project.settings.prod
```

## ⚠️ Importante

1. **NUNCA** subas archivos `.env` al repositorio
2. **SIEMPRE** usa passwords seguros en producción
3. **VERIFICA** que todas las variables estén configuradas
4. **ROTA** las contraseñas periódicamente
5. **USA** HTTPS en producción

## 🆘 Solución de Problemas

### **Error: "No such file or directory: .env"**
```bash
# Crear desde plantilla
cp env.example .env
```

### **Error: "SECRET_KEY not set"**
```bash
# Generar nueva clave
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Error: "Database connection failed"**
```bash
# Verificar configuración de base de datos
python manage.py check --database default --settings=project.settings.prod
```
