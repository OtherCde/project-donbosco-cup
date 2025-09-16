from django.db import models

from matches.models import MatchTeam
from teams.models import Player


class MatchEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ("goal", "Goal"),
        ("yellow_card", "Yellow Card"),
        ("red_card", "Red Card"),
    ]

    match_team = models.ForeignKey(
        MatchTeam, on_delete=models.CASCADE, related_name="events"
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    details = models.TextField(
        blank=True, null=True, help_text="Additional event details"
    )

    class Meta:
        verbose_name = "Evento del Partido"
        verbose_name_plural = "Eventos del Partido"

    def __str__(self):
        return f"{self.player.full_name} - {self.get_event_type_display()}"
