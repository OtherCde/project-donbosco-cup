from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Salesian Tournament 2024")
    year = models.CharField(max_length=4, help_text="Tournament year")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "Torneo"
        verbose_name_plural = "Torneos"
        ordering = ["-year", "name"]

    def __str__(self):
        return f"{self.name} - {self.year}"


class TournamentCategory(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="categories"
    )
    category_name = models.CharField(
        max_length=100, help_text="e.g., Class of 2019, Under-16"
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría del Torneo"
        verbose_name_plural = "Categorías del Torneo"
        unique_together = ["tournament", "category_name"]
        ordering = ["tournament", "category_name"]

    def __str__(self):
        return f"{self.tournament.name} - {self.category_name}"


class Phase(models.Model):
    TYPE_CHOICES = [
        ("league", "League"),
        ("knockout", "Knockout"),
    ]

    tournament_category = models.ForeignKey(
        TournamentCategory, on_delete=models.CASCADE, related_name="phases"
    )
    phase_name = models.CharField(
        max_length=100, help_text="e.g., League, Knockout, Group Stage"
    )
    phase_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Fase"
        verbose_name_plural = "Fases"
        ordering = ["tournament_category", "id"]

    def __str__(self):
        return f"{self.tournament_category} - {self.phase_name}"


class Round(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="rounds")
    round_name = models.CharField(
        max_length=100, help_text="e.g., Matchday 1, Semifinal, Final"
    )
    round_number = models.CharField(max_length=20, help_text="e.g., 1, SF, F")

    class Meta:
        verbose_name = "Ronda"
        verbose_name_plural = "Rondas"
        ordering = ["phase", "id"]

    def __str__(self):
        return f"{self.phase} - {self.round_name}"
