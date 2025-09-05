from django.db import models
from django.core.validators import MinValueValidator
from tournaments.models import Round
from teams.models import Team, Player


class Match(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='matches')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        ordering = ['date', 'time']
    
    def __str__(self):
        match_teams = self.match_teams.all()
        if match_teams.count() == 2:
            home_team = match_teams.filter(is_home=True).first()
            away_team = match_teams.filter(is_home=False).first()
            if home_team and away_team:
                return f"{home_team.team.name} vs {away_team.team.name}"
        return f"Match {self.id} - {self.date}"


class MatchTeam(models.Model):
    RESULT_CHOICES = [
        ('win', 'Win'),
        ('draw', 'Draw'),
        ('loss', 'Loss'),
    ]
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_matches')
    goals = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    penalty_goals = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, blank=True, null=True)
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Match Team"
        verbose_name_plural = "Match Teams"
        unique_together = ['match', 'team']
    
    def __str__(self):

        return f"{self.team.name} - {self.goals} goals"