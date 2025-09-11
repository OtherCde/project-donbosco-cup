"""
Admin Configuration for Teams App
================================

Este módulo configura la interfaz de administración para la gestión de equipos y jugadores.

Funcionalidades:
- Gestión de equipos por categoría de torneo
- Administración de jugadores con información personal
- Validación de DNI y números de camiseta únicos
- Cálculo automático de edad de jugadores

Uso:
1. Crear equipos dentro de una categoría específica
2. Agregar jugadores a cada equipo
3. Asignar números de camiseta y posiciones
4. Verificar información personal (DNI, fecha de nacimiento)

Notas:
- Cada equipo pertenece a una categoría específica
- Los números de camiseta deben ser únicos por equipo
- Los DNI deben ser únicos por equipo
- La edad se calcula automáticamente
"""

from django.contrib import admin

from .models import Team, Player


class PlayerInline(admin.TabularInline):
    """
    Inline para gestionar jugadores directamente desde el equipo
    
    Permite agregar jugadores sin salir de la vista del equipo.
    Campos ordenados por número de camiseta.
    """
    model = Player
    extra = 1
    fields = ['first_name', 'last_name', 'jersey_number', 'position', 'dni', 'birth_date']
    ordering = ['jersey_number']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Administración de Equipos
    
    Gestiona los equipos participantes en cada categoría del torneo.
    Ejemplo: "Promoción 1979", "Promoción 1985"
    
    Campos principales:
    - tournament_category: Categoría a la que pertenece
    - name: Nombre del equipo
    - abbreviation: Abreviatura (ej: "P79", "P85")
    - logo_url: URL del logo del equipo (opcional)
    
    Funcionalidades:
    - Inline para gestionar jugadores directamente
    - Contador automático de jugadores
    - Filtrado por torneo y categoría
    - Búsqueda por nombre y abreviatura
    
    Nota: Cada equipo representa una promoción específica
    """
    list_display = ['name', 'abbreviation', 'tournament_category', 'player_count']
    list_filter = ['tournament_category__tournament', 'tournament_category']
    search_fields = ['name', 'abbreviation']
    ordering = ['tournament_category', 'name']
    inlines = [PlayerInline]
    
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('tournament_category', 'name', 'abbreviation')
        }),
        ('Visual', {
            'fields': ('logo_url',),
            'classes': ('collapse',)
        }),
    )
    
    def player_count(self, obj):
        """Cuenta automáticamente el número de jugadores del equipo"""
        return obj.players.count()
    player_count.short_description = 'Jugadores'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Administración de Jugadores
    
    Gestiona la información personal y deportiva de cada jugador.
    
    Campos principales:
    - first_name/last_name: Nombre completo
    - birth_date: Fecha de nacimiento
    - dni: Documento Nacional de Identidad
    - team: Equipo al que pertenece
    - jersey_number: Número de camiseta
    - position: Posición en el campo
    
    Funcionalidades:
    - Cálculo automático de edad
    - Filtrado por posición, categoría y equipo
    - Búsqueda por nombre, DNI y número de camiseta
    - Validación de DNI único por equipo
    
    Validaciones:
    - DNI: 7 u 8 dígitos
    - Número de camiseta: único por equipo
    - DNI: único por equipo
    """
    list_display = ['full_name', 'jersey_number', 'team', 'position', 'age']
    list_filter = ['position', 'team__tournament_category', 'team']
    search_fields = ['first_name', 'last_name', 'dni', 'jersey_number']
    ordering = ['team', 'jersey_number']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'birth_date', 'dni')
        }),
        ('Información del Equipo', {
            'fields': ('team', 'jersey_number', 'position')
        }),
    )
    
    def age(self, obj):
        """Calcula automáticamente la edad del jugador"""
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
    age.short_description = 'Edad'
