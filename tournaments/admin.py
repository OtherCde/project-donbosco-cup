"""
Admin Configuration for Tournaments App
=======================================

Este módulo configura la interfaz de administración para la gestión de torneos.

Funcionalidades:
- Gestión de torneos principales (Copa Don Bosco 2024)
- Organización por categorías (grupos por edad/promoción)
- Configuración de fases (liga, eliminatorias)
- Administración de rondas (fechas, partidos)

Uso:
1. Crear un torneo principal (ej: "Copa Don Bosco 2024")
2. Agregar categorías (ej: "Grupo 1 (1979-1987)")
3. Configurar fases para cada categoría
4. Crear rondas dentro de cada fase

Notas:
- Las categorías se organizan por rangos de edad para competencia justa
- Las fases pueden ser "league" (todos contra todos) o "knockout" (eliminatorias)
- Las rondas permiten organizar los partidos por fechas
"""

from django.contrib import admin

from .models import Tournament, TournamentCategory, Phase, Round


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """
    Administración de Torneos Principales
    
    Permite crear y gestionar los torneos principales del sistema.
    Ejemplo: "Copa Don Bosco 2024"
    
    Campos principales:
    - name: Nombre del torneo
    - year: Año del torneo
    - start_date/end_date: Fechas de inicio y fin
    
    Funcionalidades:
    - Filtrado por año y fecha
    - Búsqueda por nombre y año
    - Jerarquía de fechas para navegación fácil
    """
    list_display = ['name', 'year', 'start_date', 'end_date']
    list_filter = ['year', 'start_date']
    search_fields = ['name', 'year']
    ordering = ['-year', 'name']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Información del Torneo', {
            'fields': ('name', 'year')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date')
        }),
    )


class PhaseInline(admin.TabularInline):
    """
    Inline para gestionar fases directamente desde la categoría
    
    Permite agregar fases (liga, eliminatorias) sin salir de la vista
    de la categoría del torneo.
    """
    model = Phase
    extra = 1
    fields = ['phase_name', 'phase_type']


@admin.register(TournamentCategory)
class TournamentCategoryAdmin(admin.ModelAdmin):
    """
    Administración de Categorías del Torneo
    
    Gestiona los grupos por edad/promoción dentro de un torneo.
    Ejemplo: "Grupo 1 (1979-1987)", "Grupo 2 (1989-1996)"
    
    Campos principales:
    - tournament: Torneo al que pertenece
    - category_name: Nombre de la categoría
    - description: Descripción opcional
    - start_date/end_date: Fechas específicas de la categoría
    
    Funcionalidades:
    - Inline para gestionar fases directamente
    - Filtrado por torneo y fecha
    - Búsqueda por nombre de categoría y torneo
    
    Nota: Cada categoría representa un grupo de equipos de edades similares
    """
    list_display = ['category_name', 'tournament', 'start_date', 'end_date']
    list_filter = ['tournament', 'start_date']
    search_fields = ['category_name', 'tournament__name']
    ordering = ['tournament', 'category_name']
    inlines = [PhaseInline]
    
    fieldsets = (
        ('Información de la Categoría', {
            'fields': ('tournament', 'category_name', 'description')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date')
        }),
    )


class RoundInline(admin.TabularInline):
    """
    Inline para gestionar rondas directamente desde la fase
    
    Permite agregar rondas (fechas, partidos) sin salir de la vista
    de la fase del torneo.
    """
    model = Round
    extra = 1
    fields = ['round_name', 'round_number']


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    """
    Administración de Fases del Torneo
    
    Gestiona las diferentes fases dentro de una categoría.
    Ejemplo: "Fase de Grupos", "Eliminatorias", "Final"
    
    Campos principales:
    - tournament_category: Categoría a la que pertenece
    - phase_name: Nombre de la fase
    - phase_type: Tipo de fase (league/knockout)
    
    Funcionalidades:
    - Inline para gestionar rondas directamente
    - Filtrado por tipo de fase y torneo
    - Búsqueda por nombre de fase y categoría
    
    Tipos de fase:
    - league: Todos contra todos (liga)
    - knockout: Eliminatorias
    """
    list_display = ['phase_name', 'tournament_category', 'phase_type']
    list_filter = ['phase_type', 'tournament_category__tournament']
    search_fields = ['phase_name', 'tournament_category__category_name']
    ordering = ['tournament_category', 'id']
    inlines = [RoundInline]


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    """
    Administración de Rondas
    
    Gestiona las rondas específicas dentro de una fase.
    Ejemplo: "Fecha 1", "Fecha 2", "Semifinal", "Final"
    
    Campos principales:
    - phase: Fase a la que pertenece
    - round_name: Nombre de la ronda
    - round_number: Número identificatorio
    
    Funcionalidades:
    - Filtrado por tipo de fase y torneo
    - Búsqueda por nombre de ronda y fase
    - Organización por fase
    
    Nota: Las rondas permiten organizar los partidos por fechas específicas
    """
    list_display = ['round_name', 'phase', 'round_number']
    list_filter = ['phase__phase_type', 'phase__tournament_category__tournament']
    search_fields = ['round_name', 'phase__phase_name']
    ordering = ['phase', 'id']
