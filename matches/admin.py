from django.contrib import admin
from django.utils.html import format_html
from .models import Match, MatchTeam


class MatchTeamInline(admin.TabularInline):
    model = MatchTeam
    extra = 2
    max_num = 2
    fields = ['team', 'goals', 'penalty_goals', 'result', 'points']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_display', 'date', 'time', 'status', 'round_info']
    list_filter = ['status', 'date', 'round__phase__tournament_category__tournament']
    search_fields = ['round__round_name', 'match_teams__team__name']
    ordering = ['date', 'time']
    date_hierarchy = 'date'
    inlines = [MatchTeamInline]
    
    fieldsets = (
        ('Match Information', {
            'fields': ('round', 'status')
        }),
        ('Schedule', {
            'fields': ('date', 'time')
        }),
    )
    
    def match_display(self, obj):
        teams = obj.match_teams.all()
        if teams.count() == 2:
            home_team = teams.filter(is_home=True).first()
            away_team = teams.filter(is_home=False).first()
            if home_team and away_team:
                return format_html(
                    '<strong>{}</strong> {} - {} <strong>{}</strong>',
                    home_team.team.name,
                    home_team.goals,
                    away_team.goals,
                    away_team.team.name
                )
        return f"Match {obj.id}"
    match_display.short_description = 'Match'
    
    def round_info(self, obj):
        return f"{obj.round.phase.tournament_category.category_name} - {obj.round.round_name}"
    round_info.short_description = 'Tournament Info'


@admin.register(MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    list_display = ['team', 'match_info', 'goals', 'penalty_goals', 'result', 'points']
    list_filter = ['result', 'match__status', 'team__tournament_category']
    search_fields = ['team__name', 'match__round__round_name']
    ordering = ['match__date', 'match__time']
    
    fieldsets = (
        ('Match Information', {
            'fields': ('match', 'team', 'is_home')
        }),
        ('Results', {
            'fields': ('goals', 'penalty_goals', 'result', 'points')
        }),
    )
    
    def match_info(self, obj):
        return f"{obj.match.date} - {obj.match.round.round_name}"
    match_info.short_description = 'Match Info'
    