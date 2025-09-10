# En este init.py añadimos la logica que se utilizara dependiendo la variable de entorno
import os

# Verify if, im DEVELOPMENT = True
DEVELOPMENT_ENVIRONMENT = os.environ.get("DEVELOPMENT_ENVIRONMENT", "False").lower() == "true"

# Enviroments deberia devolver un bool
if DEVELOPMENT_ENVIRONMENT:
    print("entorno de desarrollo")
    from .dev import *
    print("Configuración de desarrollo cargada")
else:
    print("entorno de produccion")
    from .prod import *