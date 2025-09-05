from django.contrib import admin
from django.utils.html import format_html
from .models import MatchEvent


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ['event_display', 'player', 'event_type', 'match_info']
    list_filter = ['event_type', 'match_team__match__date', 'match_team__team']
    search_fields = ['player__first_name', 'player__last_name', 'match_team__team__name']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('match_team', 'player', 'event_type')
        }),
        ('Details', {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
    )
    
    def event_display(self, obj):
        icon_map = {
            'goal': '⚽',
            'yellow_card': '🟨',
            'red_card': '🟥',
        }
        icon = icon_map.get(obj.event_type, '📝')
        return format_html('{} {}', icon, obj.get_event_type_display())
    event_display.short_description = 'Event'
    
    def match_info(self, obj):
        return f"{obj.match_team.match.date} - {obj.match_team.team.name}"
    match_info.short_description = 'Match'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'player', 'match_team__team', 'match_team__match'
        )