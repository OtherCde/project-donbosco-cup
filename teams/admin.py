from django.contrib import admin

from .models import Team, Player


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1
    fields = ['first_name', 'last_name', 'jersey_number', 'position', 'dni', 'birth_date']
    ordering = ['jersey_number']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'tournament_category', 'player_count']
    list_filter = ['tournament_category__tournament', 'tournament_category']
    search_fields = ['name', 'abbreviation']
    ordering = ['tournament_category', 'name']
    inlines = [PlayerInline]
    
    fieldsets = (
        ('Team Information', {
            'fields': ('tournament_category', 'name', 'abbreviation')
        }),
        ('Visual', {
            'fields': ('logo_url',),
            'classes': ('collapse',)
        }),
    )
    
    def player_count(self, obj):
        return obj.players.count()
    player_count.short_description = 'Players'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'jersey_number', 'team', 'position', 'age']
    list_filter = ['position', 'team__tournament_category', 'team']
    search_fields = ['first_name', 'last_name', 'dni', 'jersey_number']
    ordering = ['team', 'jersey_number']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'birth_date', 'dni')
        }),
        ('Team Information', {
            'fields': ('team', 'jersey_number', 'position')
        }),
    )
    
    def age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
    age.short_description = 'Age'
