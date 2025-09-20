from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from tournaments.models import Phase, Round, Tournament, TournamentCategory


class Command(BaseCommand):
    help = "Configura un torneo completo con grupos, fases y rondas"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tournament-name", type=str, help="Nombre del torneo", required=True
        )
        parser.add_argument("--year", type=str, help="Año del torneo", required=True)
        parser.add_argument(
            "--start-date", type=str, help="Fecha de inicio (YYYY-MM-DD)", required=True
        )
        parser.add_argument(
            "--end-date", type=str, help="Fecha de fin (YYYY-MM-DD)", required=True
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Crear torneo principal
                tournament = Tournament.objects.create(
                    name=options["tournament_name"],
                    year=options["year"],
                    start_date=options["start_date"],
                    end_date=options["end_date"],
                )

                self.stdout.write(self.style.SUCCESS(f"Torneo creado: {tournament}"))

                # Crear categorías (grupos por edad)
                groups = [
                    "Grupo 1 (1979-1987)",
                    "Grupo 2 (1989-1996)",
                    "Grupo 3 (1998-2006)",
                    "Grupo 4 (2008-2015)",
                    "Grupo 5 (2017-2023)",
                ]

                start_date = datetime.strptime(options["start_date"], "%Y-%m-%d").date()
                end_date = datetime.strptime(options["end_date"], "%Y-%m-%d").date()

                # Calcular fechas para cada grupo
                days_per_group = (end_date - start_date).days // len(groups)

                for i, group_name in enumerate(groups):
                    group_start = start_date + timedelta(days=i * days_per_group)
                    group_end = start_date + timedelta(
                        days=(i + 1) * days_per_group - 1
                    )

                    # Crear categoría
                    category = TournamentCategory.objects.create(
                        tournament=tournament,
                        category_name=group_name,
                        description=f"Grupo de equipos de promociones {group_name.split('(')[1].split(')')[0]}",
                        start_date=group_start,
                        end_date=group_end,
                    )

                    self.stdout.write(f"Categoría creada: {category}")

                    # Crear fases para cada categoría
                    self.create_phases_for_category(category, group_start, group_end)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Torneo "{tournament.name}" configurado completamente con {len(groups)} grupos'
                    )
                )

        except Exception as e:
            raise CommandError(f"Error al crear el torneo: {str(e)}")

    def create_phases_for_category(self, category, start_date, end_date):
        """Crea las fases para una categoría específica"""

        # Fase 1: Fase de Grupos (Liga)
        phase1 = Phase.objects.create(
            tournament_category=category,
            phase_name="Fase de Grupos",
            phase_type="league",
        )

        # Crear rondas para fase de grupos (4 jornadas)
        for i in range(1, 5):
            Round.objects.create(
                phase=phase1, round_name=f"Jornada {i}", round_number=str(i)
            )

        # Fase 2: Eliminatorias
        phase2 = Phase.objects.create(
            tournament_category=category,
            phase_name="Eliminatorias",
            phase_type="knockout",
        )

        # Crear rondas para eliminatorias
        knockout_rounds = [
            ("Cuartos de Final", "QF"),
            ("Semifinal", "SF"),
            ("Final", "F"),
        ]

        for round_name, round_number in knockout_rounds:
            Round.objects.create(
                phase=phase2, round_name=round_name, round_number=round_number
            )

        self.stdout.write(f"Fases creadas para {category.category_name}")
