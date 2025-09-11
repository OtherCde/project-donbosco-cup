from django.contrib import admin
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.urls import path
from django.db.models import Count
from tournaments.models import Tournament, TournamentCategory
from teams.models import Team, Player
from matches.models import Match
from events.models import MatchEvent


def admin_dashboard_view(request):
    """
    Dashboard personalizado para guiar al usuario
    """
    # Estadísticas básicas
    stats = {
        'tournaments': Tournament.objects.count(),
        'categories': TournamentCategory.objects.count(),
        'teams': Team.objects.count(),
        'players': Player.objects.count(),
        'matches': Match.objects.count(),
        'events': MatchEvent.objects.count(),
    }
    
    # Torneo más reciente
    latest_tournament = Tournament.objects.order_by('-year').first()
    
    context = {
        'stats': stats,
        'latest_tournament': latest_tournament,
    }
    
    return render(request, 'admin/dashboard.html', context)


class CopaDonBoscoAdminSite(AdminSite):
    """
    Admin personalizado con dashboard de bienvenida
    """
    site_header = "Copa Don Bosco 2024 - Administración"
    site_title = "Copa Don Bosco"
    index_title = "Panel de Administración"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', admin_dashboard_view, name='index'),
        ]
        return custom_urls + urls


# Crear instancia personalizada
admin_site = CopaDonBoscoAdminSite(name='copa_admin')

# Configuración del Admin estándar en Español
admin.site.site_header = "Copa Don Bosco 2024 - Administración"
admin.site.site_title = "Copa Don Bosco"
admin.site.index_title = "Panel de Administración"
