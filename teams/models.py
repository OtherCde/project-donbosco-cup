from django.core.validators import RegexValidator
from django.db import models

from tournaments.models import TournamentCategory


class Team(models.Model):
    tournament_category = models.ForeignKey(
        TournamentCategory, on_delete=models.CASCADE, related_name="teams"
    )
    name = models.CharField(max_length=100, help_text="Team name")
    abbreviation = models.CharField(max_length=5, help_text="e.g., BAR, RMA, BOC")
    logo_url = models.URLField(blank=True, null=True, help_text="Team logo URL")

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        unique_together = ["tournament_category", "name"]
        ordering = ["tournament_category", "name"]

    def __str__(self):
        return f"{self.name} ({self.tournament_category.category_name})"


class Player(models.Model):
    POSITION_CHOICES = [
        ("GK", "Goalkeeper"),
        ("DEF", "Defender"),
        ("MID", "Midfielder"),
        ("FWD", "Forward"),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    position = models.CharField(
        max_length=3, choices=POSITION_CHOICES, null=True, blank=True
    )
    jersey_number = models.CharField(max_length=3, null=True, blank=True)
    dni = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(regex=r"^\d{7,8}$", message="DNI must have 7 or 8 digits")
        ],
    )

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        unique_together = [["team", "jersey_number"], ["team", "dni"]]
        ordering = ["team", "jersey_number"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} (#{self.jersey_number} - {self.team.name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
