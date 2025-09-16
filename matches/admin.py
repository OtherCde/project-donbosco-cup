"""
Admin Configuration for Matches App
==================================

Este módulo configura la interfaz de administración para la gestión de partidos.

Funcionalidades:
- Gestión de partidos por ronda y fecha
- Administración de resultados de equipos
- Seguimiento de goles, tarjetas y puntos
- Visualización de partidos con formato amigable

Uso:
1. Crear partidos dentro de una ronda específica
2. Asignar equipos y horarios
3. Registrar resultados y eventos
4. Seguimiento de estadísticas por equipo

Notas:
- Cada partido pertenece a una ronda específica
- Los equipos se asignan automáticamente a los partidos
- Los resultados se calculan automáticamente
- Los puntos se asignan según el resultado
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Match, MatchTeam


class MatchTeamInline(admin.TabularInline):
    """
    Inline para gestionar equipos y resultados directamente desde el partido

    Permite asignar equipos y registrar resultados sin salir de la vista
    del partido. Máximo 2 equipos por partido.
    """

    model = MatchTeam
    extra = 2
    max_num = 2
    fields = ["team", "goals", "penalty_goals", "result", "points"]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """
    Administración de Partidos

    Gestiona los partidos del torneo con sus horarios y resultados.

    Campos principales:
    - round: Ronda a la que pertenece
    - date/time: Fecha y hora del partido
    - status: Estado del partido (scheduled, finished, cancelled)
    - match_teams: Equipos participantes y resultados

    Funcionalidades:
    - Inline para gestionar equipos y resultados
    - Visualización de partidos con formato "Equipo A 2 - 1 Equipo B"
    - Filtrado por estado, fecha y torneo
    - Búsqueda por ronda y nombre de equipo
    - Jerarquía de fechas para navegación

    Estados del partido:
    - scheduled: Programado
    - finished: Finalizado
    - cancelled: Cancelado
    """

    list_display = ["match_display", "date", "time", "status", "round_info"]
    list_filter = ["status", "date", "round__phase__tournament_category__tournament"]
    search_fields = ["round__round_name", "match_teams__team__name"]
    ordering = ["date", "time"]
    date_hierarchy = "date"
    inlines = [MatchTeamInline]

    fieldsets = (
        ("Información del Partido", {"fields": ("round", "status")}),
        ("Horario", {"fields": ("date", "time")}),
    )

    def match_display(self, obj):
        """Muestra el partido en formato 'Equipo A 2 - 1 Equipo B'"""
        teams = obj.match_teams.all()
        if teams.count() == 2:
            home_team = teams.first()
            away_team = teams.last()
            if home_team and away_team:
                return format_html(
                    "<strong>{}</strong> {} - {} <strong>{}</strong>",
                    home_team.team.name,
                    home_team.goals,
                    away_team.goals,
                    away_team.team.name,
                )
        return f"Match {obj.id}"

    match_display.short_description = "Partido"

    def round_info(self, obj):
        """Muestra información de la categoría y ronda del partido"""
        return f"{obj.round.phase.tournament_category.category_name} - {obj.round.round_name}"

    round_info.short_description = "Info del Torneo"


@admin.register(MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    """
    Administración de Equipos en Partidos

    Gestiona los resultados y estadísticas de cada equipo en los partidos.

    Campos principales:
    - match: Partido al que pertenece
    - team: Equipo participante
    - goals: Goles marcados
    - penalty_goals: Goles de penalti
    - result: Resultado (win, loss, draw)
    - points: Puntos obtenidos

    Funcionalidades:
    - Filtrado por resultado, estado del partido y categoría
    - Búsqueda por nombre de equipo y ronda
    - Seguimiento de estadísticas por equipo

    Resultados:
    - win: Victoria (3 puntos)
    - loss: Derrota (0 puntos)
    - draw: Empate (1 punto)
    """

    list_display = ["team", "match_info", "goals", "penalty_goals", "result", "points"]
    list_filter = ["result", "match__status", "team__tournament_category"]
    search_fields = ["team__name", "match__round__round_name"]
    ordering = ["match__date", "match__time"]

    fieldsets = (
        ("Información del Partido", {"fields": ("match", "team")}),
        ("Resultados", {"fields": ("goals", "penalty_goals", "result", "points")}),
    )

    def match_info(self, obj):
        """Muestra información del partido (fecha y ronda)"""
        return f"{obj.match.date} - {obj.match.round.round_name}"

    match_info.short_description = "Info del Partido"
