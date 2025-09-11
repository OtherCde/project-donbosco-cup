"""
Admin Configuration for Events App
=================================

Este módulo configura la interfaz de administración para la gestión de eventos de partidos.

Funcionalidades:
- Gestión de eventos durante los partidos (goles, tarjetas)
- Seguimiento de estadísticas por jugador
- Visualización de eventos con iconos
- Filtrado y búsqueda avanzada

Uso:
1. Registrar eventos durante los partidos
2. Asignar eventos a jugadores específicos
3. Agregar detalles adicionales si es necesario
4. Seguimiento de estadísticas por jugador

Notas:
- Cada evento pertenece a un equipo en un partido específico
- Los eventos se muestran con iconos para fácil identificación
- Se pueden agregar detalles adicionales a cada evento
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import MatchEvent


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    """
    Administración de Eventos de Partidos
    
    Gestiona todos los eventos que ocurren durante los partidos.
    
    Campos principales:
    - match_team: Equipo en el partido específico
    - player: Jugador que realizó el evento
    - event_type: Tipo de evento (gol, tarjeta amarilla, tarjeta roja)
    - details: Detalles adicionales del evento
    
    Funcionalidades:
    - Visualización de eventos con iconos
    - Filtrado por tipo de evento, fecha y equipo
    - Búsqueda por nombre de jugador y equipo
    - Optimización de consultas con select_related
    
    Tipos de eventos:
    - goal: Gol (⚽)
    - yellow_card: Tarjeta amarilla (🟨)
    - red_card: Tarjeta roja ()
    
    Nota: Los eventos se muestran con iconos para fácil identificación
    """
    list_display = ['event_display', 'player', 'event_type', 'match_info']
    list_filter = ['event_type', 'match_team__match__date', 'match_team__team']
    search_fields = ['player__first_name', 'player__last_name', 'match_team__team__name']
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('match_team', 'player', 'event_type')
        }),
        ('Detalles', {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
    )
    
    def event_display(self, obj):
        """Muestra el evento con su icono correspondiente"""
        icon_map = {
            'goal': '⚽',
            'yellow_card': '',
            'red_card': '',
        }
        icon = icon_map.get(obj.event_type, '📝')
        return format_html('{} {}', icon, obj.get_event_type_display())
    event_display.short_description = 'Evento'
    
    def match_info(self, obj):
        """Muestra información del partido (fecha y equipo)"""
        return f"{obj.match_team.match.date} - {obj.match_team.team.name}"
    match_info.short_description = 'Partido'
    
    def get_queryset(self, request):
        """Optimiza las consultas para mejor rendimiento"""
        return super().get_queryset(request).select_related(
            'player', 'match_team__team', 'match_team__match'
        )