from django.contrib import admin

from .models import Tournament, TournamentCategory, Phase, Round


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'start_date', 'end_date']
    list_filter = ['year', 'start_date']
    search_fields = ['name', 'year']
    ordering = ['-year', 'name']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Tournament Information', {
            'fields': ('name', 'year')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
    )


class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 1
    fields = ['phase_name', 'phase_type']


@admin.register(TournamentCategory)
class TournamentCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'tournament', 'start_date', 'end_date']
    list_filter = ['tournament', 'start_date']
    search_fields = ['category_name', 'tournament__name']
    ordering = ['tournament', 'category_name']
    inlines = [PhaseInline]
    
    fieldsets = (
        ('Category Information', {
            'fields': ('tournament', 'category_name', 'description')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
    )


class RoundInline(admin.TabularInline):
    model = Round
    extra = 1
    fields = ['round_name', 'round_number']


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ['phase_name', 'tournament_category', 'phase_type']
    list_filter = ['phase_type', 'tournament_category__tournament']
    search_fields = ['phase_name', 'tournament_category__category_name']
    ordering = ['tournament_category', 'id']
    inlines = [RoundInline]


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['round_name', 'phase', 'round_number']
    list_filter = ['phase__phase_type', 'phase__tournament_category__tournament']
    search_fields = ['round_name', 'phase__phase_name']
    ordering = ['phase', 'id']
