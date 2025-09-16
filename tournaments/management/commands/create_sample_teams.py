import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from teams.models import Team
from tournaments.models import TournamentCategory


class Command(BaseCommand):
    help = "Crea equipos de ejemplo para cada categoría basados en las promociones"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tournament-category-id",
            type=int,
            help="ID de la categoría del torneo",
            required=True,
        )

    def handle(self, *args, **options):
        try:
            category = TournamentCategory.objects.get(
                id=options["tournament_category_id"]
            )

            # Definir promociones por grupo basado en la imagen
            promotions_by_group = {
                "Grupo 1 (1979-1987)": ["1979", "1982", "1985", "1986", "1987"],
                "Grupo 2 (1989-1996)": ["1989", "1992", "1993", "1994", "1996"],
                "Grupo 3 (1998-2006)": ["1998", "2000", "2004", "2005", "2006"],
                "Grupo 4 (2008-2015)": [
                    "2008",
                    "2010",
                    "2013",
                    "2014",
                    "2015A",
                    "2015B",
                ],
                "Grupo 5 (2017-2023)": [
                    "2017",
                    "2019",
                    "2020A",
                    "2020B",
                    "2021",
                    "2023",
                ],
            }

            # Obtener promociones para este grupo
            group_name = category.category_name
            if group_name not in promotions_by_group:
                raise CommandError(
                    f"No se encontraron promociones para el grupo: {group_name}"
                )

            promotions = promotions_by_group[group_name]

            with transaction.atomic():
                teams_created = 0

                for promotion in promotions:
                    # Crear equipo para cada promoción
                    team_name = f"Promoción {promotion}"
                    abbreviation = f"P{promotion.replace('A', '').replace('B', '')}"

                    # Si ya existe, no crear duplicado
                    if not Team.objects.filter(
                        tournament_category=category, name=team_name
                    ).exists():
                        Team.objects.create(
                            tournament_category=category,
                            name=team_name,
                            abbreviation=abbreviation,
                            logo_url="",  # Se puede agregar URL de logo después
                        )
                        teams_created += 1
                        self.stdout.write(f"Equipo creado: {team_name}")

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Creados {teams_created} equipos para {category.category_name}"
                    )
                )

        except TournamentCategory.DoesNotExist:
            raise CommandError("Categoría de torneo no encontrada")
        except Exception as e:
            raise CommandError(f"Error al crear equipos: {str(e)}")
