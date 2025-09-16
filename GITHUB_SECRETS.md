# 🔐 GitHub Secrets - Configuración Requerida

## 📋 Variables de GitHub Secrets Necesarias

Para que los workflows funcionen correctamente, necesitas configurar las siguientes variables en GitHub Secrets:

### 🗄️ **Base de Datos PostgreSQL**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `DB_NAME` | Nombre de la base de datos | `donbosco_cup_prod` | ✅ |
| `DB_USER` | Usuario de la base de datos | `postgres` | ✅ |
| `DB_PASSWORD` | Contraseña de la base de datos | `tu-password-seguro` | ✅ |
| `DB_HOST` | Host de la base de datos | `localhost` o `db.example.com` | ✅ |
| `DB_PORT` | Puerto de la base de datos | `5432` | ✅ |

### 🔑 **Django**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `SECRET_KEY` | Clave secreta de Django | `django-secret-key-muy-largo-y-seguro` | ✅ |

### 🌐 **Configuración Web**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `ALLOWED_HOSTS` | Hosts permitidos (separados por comas) | `example.com,www.example.com` | ✅ |
| `CSRF_TRUSTED_ORIGINS` | Orígenes confiables para CSRF | `https://example.com,https://www.example.com` | ✅ |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS | `https://frontend.example.com` | ✅ |

### 🔒 **Seguridad**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `SESSION_COOKIE_SECURE` | Cookies seguras | `True` | ✅ |
| `CSRF_COOKIE_SECURE` | Cookies CSRF seguras | `True` | ✅ |
| `SECURE_SSL_REDIRECT` | Redirección SSL | `True` | ✅ |

### 📧 **Email (Opcional)**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `EMAIL_HOST` | Servidor SMTP | `smtp.sendgrid.net` | ❌ |
| `EMAIL_PORT` | Puerto SMTP | `587` | ❌ |
| `EMAIL_USE_TLS` | Usar TLS | `True` | ❌ |
| `EMAIL_HOST_USER` | Usuario SMTP | `apikey` | ❌ |
| `EMAIL_HOST_PASSWORD` | Contraseña SMTP | `SG.tu-api-key` | ❌ |
| `DEFAULT_FROM_EMAIL` | Email remitente | `noreply@example.com` | ❌ |

### 🚀 **Deployment (Opcional)**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `DOCKER_USERNAME` | Usuario de Docker Hub | `tu-usuario` | ❌ |
| `DOCKER_PASSWORD` | Contraseña de Docker Hub | `tu-password` | ❌ |
| `DEPLOY_HOST` | Host de deployment | `tu-servidor.com` | ❌ |
| `DEPLOY_USER` | Usuario SSH | `deploy` | ❌ |
| `DEPLOY_KEY` | Clave privada SSH | `-----BEGIN OPENSSH PRIVATE KEY-----` | ❌ |

### 📊 **Monitoreo (Opcional)**

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `SENTRY_DSN` | DSN de Sentry | `https://key@sentry.io/project` | ❌ |
| `CODECOV_TOKEN` | Token de Codecov | `tu-token` | ❌ |

## 🔧 **Cómo Configurar GitHub Secrets**

### 1. **Acceder a la Configuración**
1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings**
3. En el menú lateral, haz clic en **Secrets and variables** → **Actions**

### 2. **Agregar Secrets**
1. Haz clic en **New repository secret**
2. Ingresa el **Name** (nombre de la variable)
3. Ingresa el **Secret** (valor de la variable)
4. Haz clic en **Add secret**

### 3. **Verificar Configuración**
Puedes verificar que los secrets estén configurados correctamente ejecutando el workflow de setup.

## 🚨 **Variables Críticas para Producción**

### **OBLIGATORIAS:**
- `SECRET_KEY` - **CRÍTICO**: Debe ser única y segura
- `DB_PASSWORD` - **CRÍTICO**: Contraseña fuerte de la base de datos
- `ALLOWED_HOSTS` - **IMPORTANTE**: Debe incluir tu dominio
- `CSRF_TRUSTED_ORIGINS` - **IMPORTANTE**: Para seguridad CSRF

### **RECOMENDADAS:**
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_SSL_REDIRECT=True`

## 🔐 **Generar SECRET_KEY Segura**

Puedes generar una SECRET_KEY segura usando Python:

```python
import secrets
import string

# Generar clave de 50 caracteres
chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(chars) for _ in range(50))
print(secret_key)
```

O usando Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📝 **Ejemplo de Configuración Completa**

```bash
# Variables obligatorias
SECRET_KEY=django-insecure-your-very-long-and-secure-secret-key-here
DB_NAME=donbosco_cup_prod
DB_USER=postgres
DB_PASSWORD=your-very-secure-database-password
DB_HOST=db.example.com
DB_PORT=5432
ALLOWED_HOSTS=example.com,www.example.com,api.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
CORS_ALLOWED_ORIGINS=https://frontend.example.com

# Variables de seguridad
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# Variables opcionales
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@example.com
```

## ⚠️ **Importante**

1. **NUNCA** subas archivos `.env` al repositorio
2. **SIEMPRE** usa valores únicos y seguros en producción
3. **ROTA** las contraseñas periódicamente
4. **VERIFICA** que los secrets estén configurados antes del deployment
5. **USA** HTTPS en producción
6. **CONFIGURA** correctamente los dominios en `ALLOWED_HOSTS`

## 🔍 **Verificación de Configuración**

El workflow `setup-environment.yml` verificará automáticamente que todas las variables necesarias estén configuradas y funcionando correctamente.
