"""
API App Configuration
====================

Configuración de la aplicación API para Don Bosco Cup.
Este módulo contiene toda la funcionalidad de la API REST.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuración de la aplicación API"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    verbose_name = "Don Bosco Cup API"

    def ready(self):
        """Inicialización de la aplicación API"""
        pass
