"""
URLs para Don Bosco Cup API
==========================

Este módulo define todas las rutas de la API REST para la aplicación.
Incluye endpoints para todos los modelos con CRUD completo.

Endpoints disponibles:
- /api/tournaments/ - Gestión de torneos
- /api/categories/ - Gestión de categorías
- /api/phases/ - Gestión de fases
- /api/rounds/ - Gestión de rondas
- /api/teams/ - Gestión de equipos
- /api/players/ - Gestión de jugadores
- /api/matches/ - Gestión de partidos
- /api/match-teams/ - Gestión de equipos en partidos
- /api/events/ - Gestión de eventos de partidos
- /api/users/ - Consulta de usuarios (solo lectura)

Autenticación:
- JWT Token requerido para todos los endpoints
- Permisos por grupo de usuario (CRUD_Users, ReadOnly_Users)
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.viewsets.base import (
    MatchEventViewSet,
    MatchTeamViewSet,
    MatchViewSet,
    PhaseViewSet,
    PlayerViewSet,
    RoundViewSet,
    TeamViewSet,
    TournamentCategoryViewSet,
    TournamentViewSet,
    UserViewSet,
)

# Crear el router de DRF
router = DefaultRouter()

# Registrar todos los ViewSets
router.register(r"tournaments", TournamentViewSet, basename="tournament")
router.register(r"categories", TournamentCategoryViewSet, basename="tournamentcategory")
router.register(r"phases", PhaseViewSet, basename="phase")
router.register(r"rounds", RoundViewSet, basename="round")
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"matches", MatchViewSet, basename="match")
router.register(r"match-teams", MatchTeamViewSet, basename="matchteam")
router.register(r"events", MatchEventViewSet, basename="matchevent")
router.register(r"users", UserViewSet, basename="user")

# URLs de la API
urlpatterns = [
    # URLs del router (todos los endpoints CRUD)
    path("", include(router.urls)),
    # URLs de autenticación JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # URLs adicionales para funcionalidades específicas
    path(
        "auth/", include("rest_framework.urls")
    ),  # Para autenticación en browsable API
]
