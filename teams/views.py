from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import ExcelPlayerUploadForm
from .models import Player
from .utils import (
    auto_assign_dni,
    auto_assign_jersey_numbers,
    extract_players_from_excel,
)


@staff_member_required
def upload_players_from_excel(request):
    if request.method == "POST":
        form = ExcelPlayerUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                team = form.cleaned_data["team"]
                excel_file = form.cleaned_data["excel_file"]
                header_row = form.cleaned_data["header_row"]
                start_data_row = form.cleaned_data["start_data_row"]
                default_position = form.cleaned_data["default_position"]

                # Extraer jugadores del Excel
                players_data = extract_players_from_excel(
                    excel_file, header_row, start_data_row, default_position
                )

                if not players_data:
                    messages.warning(
                        request, "No se encontraron jugadores en el archivo Excel."
                    )
                    return render(
                        request, "admin/teams/upload_players.html", {"form": form}
                    )

                # Asignar números y DNI automáticamente si es necesario
                auto_assign_jersey_numbers(players_data, team)
                auto_assign_dni(players_data, team)

                # Crear jugadores
                created_players = []
                errors = []
                skipped_players = []

                for player_data in players_data:
                    try:
                        # Verificar si ya existe un jugador con el mismo DNI en el equipo
                        if Player.objects.filter(
                            team=team, dni=player_data["dni"]
                        ).exists():
                            skipped_players.append(
                                f"{player_data['first_name']} {player_data['last_name']} (DNI ya existe)"
                            )
                            continue

                        # Verificar si ya existe un jugador con el mismo número de camiseta
                        if Player.objects.filter(
                            team=team, jersey_number=player_data["jersey_number"]
                        ).exists():
                            errors.append(
                                f"Número de camiseta {player_data['jersey_number']} ya está en uso para {player_data['first_name']} {player_data['last_name']}"
                            )
                            continue

                        player = Player.objects.create(
                            team=team,
                            first_name=player_data["first_name"],
                            last_name=player_data["last_name"],
                            jersey_number=player_data["jersey_number"],
                            position=player_data["position"],
                            birth_date=player_data["birth_date"],
                            dni=player_data["dni"],
                        )
                        created_players.append(player)

                    except Exception as e:
                        errors.append(
                            f"Error creando jugador {player_data['first_name']} {player_data['last_name']} (fila {player_data.get('row_number', '?')}): {str(e)}"
                        )

                # Mostrar resultados
                if created_players:
                    messages.success(
                        request,
                        f"✅ Se crearon {len(created_players)} jugadores exitosamente.",
                    )

                if skipped_players:
                    messages.info(
                        request,
                        f"⚠️ Se omitieron {len(skipped_players)} jugadores que ya existían.",
                    )
                    for skip in skipped_players[:5]:  # Mostrar solo los primeros 5
                        messages.info(request, f"Omitido: {skip}")

                if errors:
                    messages.error(request, f"❌ Se encontraron {len(errors)} errores:")
                    for error in errors[:5]:  # Mostrar solo los primeros 5 errores
                        messages.error(request, error)

                return redirect("admin:teams_team_changelist")

            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error procesando el archivo: {str(e)}")

    else:
        form = ExcelPlayerUploadForm()

    return render(request, "admin/teams/upload_players.html", {"form": form})
