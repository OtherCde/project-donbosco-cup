"""
ViewSets para Don Bosco Cup API
==============================

Este módulo define los ViewSets para todos los modelos de la aplicación.
Implementa CRUD completo con permisos personalizados y filtros avanzados.

Funcionalidades:
- ViewSets para todos los modelos con CRUD completo
- Permisos personalizados por grupo de usuario
- Filtros y búsquedas avanzadas
- Paginación automática
- Métodos personalizados para operaciones específicas
"""

from django.contrib.auth.models import User
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions.base import IsAdminOrCRUDUser, IsCRUDOrReadOnlyUser
from api.serializers.base import (
    MatchEventSerializer,
    MatchSerializer,
    MatchTeamSerializer,
    MatchWithDetailsSerializer,
    PhaseSerializer,
    PlayerSerializer,
    RoundSerializer,
    TeamSerializer,
    TeamWithPlayersSerializer,
    TournamentCategorySerializer,
    TournamentSerializer,
    UserSerializer,
)
from events.models import MatchEvent
from matches.models import Match, MatchTeam
from teams.models import Player, Team
from tournaments.models import Phase, Round, Tournament, TournamentCategory

# =============================================================================
# VIEWSETS PARA TOURNAMENTS
# =============================================================================


class TournamentViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Tournament"""

    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["year", "start_date", "end_date"]
    search_fields = ["name", "year"]
    ordering_fields = ["name", "year", "start_date", "end_date"]
    ordering = ["-year", "name"]

    @action(detail=True, methods=["get"])
    def categories(self, request, pk=None):
        """Obtener todas las categorías de un torneo"""
        tournament = self.get_object()
        categories = tournament.categories.all()
        serializer = TournamentCategorySerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def current(self, request):
        """Obtener el torneo actual (más reciente)"""
        current_tournament = Tournament.objects.filter(
            start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date()
        ).first()

        if not current_tournament:
            current_tournament = Tournament.objects.order_by("-year").first()

        if current_tournament:
            serializer = self.get_serializer(current_tournament)
            return Response(serializer.data)
        return Response(
            {"message": "No hay torneo actual"}, status=status.HTTP_404_NOT_FOUND
        )


class TournamentCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo TournamentCategory"""

    queryset = TournamentCategory.objects.all()
    serializer_class = TournamentCategorySerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["tournament", "start_date", "end_date"]
    search_fields = ["category_name", "description", "tournament__name"]
    ordering_fields = ["category_name", "start_date", "end_date"]
    ordering = ["tournament", "category_name"]

    @action(detail=True, methods=["get"])
    def teams(self, request, pk=None):
        """Obtener todos los equipos de una categoría"""
        category = self.get_object()
        teams = category.teams.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class PhaseViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Phase"""

    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["tournament_category", "phase_type"]
    search_fields = ["phase_name", "tournament_category__category_name"]
    ordering_fields = ["phase_name", "id"]
    ordering = ["tournament_category", "id"]


class RoundViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Round"""

    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["phase", "phase__phase_type"]
    search_fields = ["round_name", "phase__phase_name"]
    ordering_fields = ["round_name", "round_number", "id"]
    ordering = ["phase", "id"]


# =============================================================================
# VIEWSETS PARA TEAMS
# =============================================================================


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Team"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["tournament_category", "tournament_category__tournament"]
    search_fields = ["name", "abbreviation", "tournament_category__category_name"]
    ordering_fields = ["name", "abbreviation"]
    ordering = ["tournament_category", "name"]

    @action(detail=True, methods=["get"])
    def players(self, request, pk=None):
        """Obtener todos los jugadores de un equipo"""
        team = self.get_object()
        players = team.players.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def with_players(self, request, pk=None):
        """Obtener equipo con todos sus jugadores"""
        team = self.get_object()
        serializer = TeamWithPlayersSerializer(team)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_tournament(self, request):
        """Obtener equipos filtrados por torneo"""
        tournament_id = request.query_params.get("tournament_id")
        if tournament_id:
            teams = Team.objects.filter(
                tournament_category__tournament_id=tournament_id
            )
            serializer = self.get_serializer(teams, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "tournament_id es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )


class PlayerViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Player"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "team",
        "position",
        "promo",
        "oficio",
        "team__tournament_category",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "dni",
        "jersey_number",
        "telefono",
        "oficio",
    ]
    ordering_fields = ["first_name", "last_name", "jersey_number", "birth_date"]
    ordering = ["team", "jersey_number"]

    @action(detail=False, methods=["get"])
    def by_team(self, request):
        """Obtener jugadores filtrados por equipo"""
        team_id = request.query_params.get("team_id")
        if team_id:
            players = Player.objects.filter(team_id=team_id)
            serializer = self.get_serializer(players, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "team_id es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["get"])
    def by_position(self, request):
        """Obtener jugadores filtrados por posición"""
        position = request.query_params.get("position")
        if position:
            players = Player.objects.filter(position=position)
            serializer = self.get_serializer(players, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "position es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )


# =============================================================================
# VIEWSETS PARA MATCHES
# =============================================================================


class MatchViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Match"""

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["round", "status", "date", "round__phase__tournament_category"]
    search_fields = ["round__round_name", "match_teams__team__name"]
    ordering_fields = ["date", "time", "status"]
    ordering = ["date", "time"]

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        """Obtener partido con todos sus detalles"""
        match = self.get_object()
        serializer = MatchWithDetailsSerializer(match)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_date(self, request):
        """Obtener partidos filtrados por fecha"""
        date = request.query_params.get("date")
        if date:
            matches = Match.objects.filter(date=date)
            serializer = self.get_serializer(matches, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "date es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["get"])
    def by_status(self, request):
        """Obtener partidos filtrados por estado"""
        status = request.query_params.get("status")
        if status:
            matches = Match.objects.filter(status=status)
            serializer = self.get_serializer(matches, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "status es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )


class MatchTeamViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo MatchTeam"""

    queryset = MatchTeam.objects.all()
    serializer_class = MatchTeamSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["match", "team", "result", "match__status"]
    search_fields = ["team__name", "match__round__round_name"]
    ordering_fields = ["goals", "points", "match__date"]
    ordering = ["match__date", "match__time"]

    @action(detail=False, methods=["get"])
    def by_team(self, request):
        """Obtener partidos de un equipo específico"""
        team_id = request.query_params.get("team_id")
        if team_id:
            match_teams = MatchTeam.objects.filter(team_id=team_id)
            serializer = self.get_serializer(match_teams, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "team_id es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )


# =============================================================================
# VIEWSETS PARA EVENTS
# =============================================================================


class MatchEventViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo MatchEvent"""

    queryset = MatchEvent.objects.all()
    serializer_class = MatchEventSerializer
    permission_classes = [IsCRUDOrReadOnlyUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["match_team", "player", "event_type", "match_team__team"]
    search_fields = ["player__first_name", "player__last_name", "details"]
    ordering_fields = ["event_type", "id"]
    ordering = ["match_team__match__date", "id"]

    @action(detail=False, methods=["get"])
    def by_player(self, request):
        """Obtener eventos de un jugador específico"""
        player_id = request.query_params.get("player_id")
        if player_id:
            events = MatchEvent.objects.filter(player_id=player_id)
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "player_id es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["get"])
    def by_match(self, request):
        """Obtener eventos de un partido específico"""
        match_id = request.query_params.get("match_id")
        if match_id:
            events = MatchEvent.objects.filter(match_team__match_id=match_id)
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "match_id es requerido"}, status=status.HTTP_400_BAD_REQUEST
        )


# =============================================================================
# VIEWSET PARA USUARIOS
# =============================================================================


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para el modelo User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrCRUDUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["groups"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering_fields = ["username", "first_name", "last_name"]
    ordering = ["username"]
