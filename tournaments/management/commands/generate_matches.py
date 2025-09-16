import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from matches.models import Match, MatchTeam
from teams.models import Team
from tournaments.models import Phase, Round, Tournament, TournamentCategory


class Command(BaseCommand):
    help = "Genera partidos automáticamente para una fase específica"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tournament-category-id",
            type=int,
            help="ID de la categoría del torneo",
            required=True,
        )
        parser.add_argument("--phase-id", type=int, help="ID de la fase", required=True)
        parser.add_argument(
            "--round-id", type=int, help="ID de la ronda", required=True
        )
        parser.add_argument(
            "--start-date", type=str, help="Fecha de inicio (YYYY-MM-DD)", required=True
        )
        parser.add_argument(
            "--days-between-matches",
            type=int,
            default=7,
            help="Días entre partidos (default: 7)",
        )

    def handle(self, *args, **options):
        try:
            # Obtener objetos
            tournament_category = TournamentCategory.objects.get(
                id=options["tournament_category_id"]
            )
            phase = Phase.objects.get(id=options["phase_id"])
            round_obj = Round.objects.get(id=options["round_id"])

            # Verificar que la ronda pertenece a la fase
            if round_obj.phase != phase:
                raise CommandError("La ronda no pertenece a la fase especificada")

            # Verificar que la fase pertenece a la categoría
            if phase.tournament_category != tournament_category:
                raise CommandError("La fase no pertenece a la categoría especificada")

            # Obtener equipos de la categoría
            teams = Team.objects.filter(tournament_category=tournament_category)

            if len(teams) < 2:
                raise CommandError(
                    "Se necesitan al menos 2 equipos para generar partidos"
                )

            # Generar partidos según el tipo de fase
            if phase.phase_type == "league":
                self.generate_league_matches(
                    round_obj,
                    teams,
                    options["start_date"],
                    options["days_between_matches"],
                )
            elif phase.phase_type == "knockout":
                self.generate_knockout_matches(
                    round_obj,
                    teams,
                    options["start_date"],
                    options["days_between_matches"],
                )
            else:
                raise CommandError("Tipo de fase no soportado")

            self.stdout.write(
                self.style.SUCCESS(
                    f"Partidos generados exitosamente para {tournament_category.category_name} - {phase.phase_name} - {round_obj.round_name}"
                )
            )

        except TournamentCategory.DoesNotExist:
            raise CommandError("Categoría de torneo no encontrada")
        except Phase.DoesNotExist:
            raise CommandError("Fase no encontrada")
        except Round.DoesNotExist:
            raise CommandError("Ronda no encontrada")

    def generate_league_matches(self, round_obj, teams, start_date, days_between):
        """Genera partidos para fase de liga (todos contra todos)"""
        with transaction.atomic():
            # Crear lista de equipos y mezclar
            teams_list = list(teams)
            random.shuffle(teams_list)

            # Generar partidos (todos contra todos)
            matches_created = 0
            current_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            for i in range(len(teams_list)):
                for j in range(i + 1, len(teams_list)):
                    # Crear partido
                    match = Match.objects.create(
                        round=round_obj,
                        date=current_date,
                        time=datetime.strptime("15:00", "%H:%M").time(),
                        status="scheduled",
                    )

                    # Crear MatchTeam para cada equipo
                    MatchTeam.objects.create(
                        match=match,
                        team=teams_list[i],
                        goals=0,
                        penalty_goals=0,
                        points=0,
                    )

                    MatchTeam.objects.create(
                        match=match,
                        team=teams_list[j],
                        goals=0,
                        penalty_goals=0,
                        points=0,
                    )

                    matches_created += 1

                    # Avanzar fecha cada 2 partidos
                    if matches_created % 2 == 0:
                        current_date += timedelta(days=days_between)

            self.stdout.write(f"Creados {matches_created} partidos de liga")

    def generate_knockout_matches(self, round_obj, teams, start_date, days_between):
        """Genera partidos para fase eliminatoria"""
        with transaction.atomic():
            teams_list = list(teams)
            random.shuffle(teams_list)

            # Verificar que el número de equipos sea potencia de 2
            num_teams = len(teams_list)
            if num_teams & (num_teams - 1) != 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"El número de equipos ({num_teams}) no es potencia de 2. "
                        "Algunos equipos tendrán bye en la primera ronda."
                    )
                )

            current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            matches_created = 0

            # Crear partidos por parejas
            for i in range(0, len(teams_list), 2):
                if i + 1 < len(teams_list):
                    # Crear partido
                    match = Match.objects.create(
                        round=round_obj,
                        date=current_date,
                        time=datetime.strptime("15:00", "%H:%M").time(),
                        status="scheduled",
                    )

                    # Crear MatchTeam para cada equipo
                    MatchTeam.objects.create(
                        match=match,
                        team=teams_list[i],
                        goals=0,
                        penalty_goals=0,
                        points=0,
                    )

                    MatchTeam.objects.create(
                        match=match,
                        team=teams_list[i + 1],
                        goals=0,
                        penalty_goals=0,
                        points=0,
                    )

                    matches_created += 1
                    current_date += timedelta(days=days_between)

            self.stdout.write(f"Creados {matches_created} partidos eliminatorios")
