"""
Serializers para Don Bosco Cup API
=================================

Este módulo define los serializers para todos los modelos de la aplicación.
Incluye validaciones personalizadas y relaciones anidadas para una API robusta.

Funcionalidades:
- Serializers para todos los modelos (Tournament, Team, Player, Match, etc.)
- Validaciones personalizadas
- Relaciones anidadas para facilitar el uso de la API
- Serializers de solo lectura para consultas rápidas
"""

from rest_framework import serializers
from django.contrib.auth.models import User

from tournaments.models import Tournament, TournamentCategory, Phase, Round
from teams.models import Team, Player
from matches.models import Match, MatchTeam
from events.models import MatchEvent


# =============================================================================
# SERIALIZERS PARA TOURNAMENTS
# =============================================================================

class TournamentSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Tournament"""
    
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'year', 'start_date', 'end_date']
        read_only_fields = ['id']
    
    def validate(self, data):
        """Validar que la fecha de inicio sea anterior a la fecha de fin"""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser anterior a la fecha de fin"
            )
        return data


class TournamentCategorySerializer(serializers.ModelSerializer):
    """Serializer para el modelo TournamentCategory"""
    
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)
    
    class Meta:
        model = TournamentCategory
        fields = [
            'id', 'tournament', 'tournament_name', 'category_name', 
            'description', 'start_date', 'end_date'
        ]
        read_only_fields = ['id']
    
    def validate(self, data):
        """Validar fechas y unicidad"""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser anterior a la fecha de fin"
            )
        return data


class PhaseSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Phase"""
    
    tournament_category_name = serializers.CharField(
        source='tournament_category.category_name', read_only=True
    )
    
    class Meta:
        model = Phase
        fields = [
            'id', 'tournament_category', 'tournament_category_name', 
            'phase_name', 'phase_type'
        ]
        read_only_fields = ['id']


class RoundSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Round"""
    
    phase_name = serializers.CharField(source='phase.phase_name', read_only=True)
    tournament_category_name = serializers.CharField(
        source='phase.tournament_category.category_name', read_only=True
    )
    
    class Meta:
        model = Round
        fields = [
            'id', 'phase', 'phase_name', 'round_name', 'round_number',
            'tournament_category_name'
        ]
        read_only_fields = ['id']


# =============================================================================
# SERIALIZERS PARA TEAMS
# =============================================================================

class TeamSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Team"""
    
    tournament_category_name = serializers.CharField(
        source='tournament_category.category_name', read_only=True
    )
    tournament_name = serializers.CharField(
        source='tournament_category.tournament.name', read_only=True
    )
    player_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'tournament_category', 'tournament_category_name', 
            'tournament_name', 'name', 'abbreviation', 'logo_url', 'player_count'
        ]
        read_only_fields = ['id', 'player_count']
    
    def get_player_count(self, obj):
        """Obtener el número de jugadores del equipo"""
        return obj.players.count()


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Player"""
    
    team_name = serializers.CharField(source='team.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'team', 'team_name', 'first_name', 'last_name', 
            'full_name', 'birth_date', 'age', 'position', 'jersey_number',
            'dni', 'telefono', 'promo', 'oficio'
        ]
        read_only_fields = ['id', 'team_name', 'full_name', 'age']
    
    def get_full_name(self, obj):
        """Obtener el nombre completo del jugador"""
        return f"{obj.first_name} {obj.last_name}"
    
    def get_age(self, obj):
        """Calcular la edad del jugador"""
        from datetime import date
        today = date.today()
        return (
            today.year - obj.birth_date.year - 
            ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
        )
    
    def validate(self, data):
        """Validar unicidad de DNI y número de camiseta por equipo"""
        team = data.get('team')
        jersey_number = data.get('jersey_number')
        dni = data.get('dni')
        
        if team and jersey_number:
            # Verificar que el número de camiseta sea único en el equipo
            existing_player = Player.objects.filter(
                team=team, jersey_number=jersey_number
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_player.exists():
                raise serializers.ValidationError(
                    f"Ya existe un jugador con el número {jersey_number} en este equipo"
                )
        
        if team and dni:
            # Verificar que el DNI sea único en el equipo
            existing_player = Player.objects.filter(
                team=team, dni=dni
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_player.exists():
                raise serializers.ValidationError(
                    f"Ya existe un jugador con el DNI {dni} en este equipo"
                )
        
        return data


# =============================================================================
# SERIALIZERS PARA MATCHES
# =============================================================================

class MatchSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Match"""
    
    round_name = serializers.CharField(source='round.round_name', read_only=True)
    tournament_category_name = serializers.CharField(
        source='round.phase.tournament_category.category_name', read_only=True
    )
    match_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = [
            'id', 'round', 'round_name', 'date', 'time', 'status',
            'tournament_category_name', 'match_display'
        ]
        read_only_fields = ['id', 'round_name', 'tournament_category_name', 'match_display']
    
    def get_match_display(self, obj):
        """Obtener la representación del partido"""
        teams = obj.match_teams.all()
        if teams.count() == 2:
            home_team = teams.first()
            away_team = teams.last()
            if home_team and away_team:
                return f"{home_team.team.name} vs {away_team.team.name}"
        return f"Match {obj.id}"


class MatchTeamSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MatchTeam"""
    
    team_name = serializers.CharField(source='team.name', read_only=True)
    match_info = serializers.SerializerMethodField()
    
    class Meta:
        model = MatchTeam
        fields = [
            'id', 'match', 'team', 'team_name', 'goals', 'penalty_goals',
            'result', 'points', 'match_info'
        ]
        read_only_fields = ['id', 'team_name', 'match_info']
    
    def get_match_info(self, obj):
        """Obtener información del partido"""
        return f"{obj.match.date} - {obj.match.round.round_name}"


# =============================================================================
# SERIALIZERS PARA EVENTS
# =============================================================================

class MatchEventSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MatchEvent"""
    
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    team_name = serializers.CharField(source='match_team.team.name', read_only=True)
    match_info = serializers.SerializerMethodField()
    
    class Meta:
        model = MatchEvent
        fields = [
            'id', 'match_team', 'player', 'player_name', 'team_name',
            'event_type', 'details', 'match_info'
        ]
        read_only_fields = ['id', 'player_name', 'team_name', 'match_info']
    
    def get_match_info(self, obj):
        """Obtener información del partido"""
        return f"{obj.match_team.match.date} - {obj.match_team.match.round.round_name}"


# =============================================================================
# SERIALIZERS DE USUARIO
# =============================================================================

class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    
    groups = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups']
        read_only_fields = ['id', 'groups']


# =============================================================================
# SERIALIZERS ANIDADOS PARA CONSULTAS COMPLEJAS
# =============================================================================

class TeamWithPlayersSerializer(TeamSerializer):
    """Serializer de equipo con jugadores incluidos"""
    
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['players']


class MatchWithDetailsSerializer(MatchSerializer):
    """Serializer de partido con equipos y eventos incluidos"""
    
    match_teams = MatchTeamSerializer(many=True, read_only=True)
    
    class Meta(MatchSerializer.Meta):
        fields = MatchSerializer.Meta.fields + ['match_teams']
