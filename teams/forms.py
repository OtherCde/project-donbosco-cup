from django import forms
from django.core.exceptions import ValidationError
from .models import Team


class ExcelPlayerUploadForm(forms.Form):
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="Equipo",
        help_text="Selecciona el equipo al que pertenecen los jugadores",
    )
    excel_file = forms.FileField(
        label="Archivo Excel",
        help_text="Sube el archivo Excel (.xlsx) con los datos de los jugadores",
    )

    # Opciones de configuración
    header_row = forms.IntegerField(
        initial=24,
        label="Fila de encabezados",
        help_text="Número de fila donde están los encabezados (por defecto: 24)",
    )

    start_data_row = forms.IntegerField(
        initial=25,
        label="Fila de inicio de datos",
        help_text="Número de fila donde comienzan los datos de jugadores (por defecto: 25)",
    )

    default_position = forms.ChoiceField(
        choices=[
            ("MID", "Mediocampo"),
            ("FWD", "Delantero"),
            ("DEF", "Defensa"),
            ("GK", "Portero"),
        ],
        initial="MID",
        label="Posición por defecto",
        help_text="Posición que se asignará a todos los jugadores",
    )

    def clean_excel_file(self):
        file = self.cleaned_data["excel_file"]
        if not file.name.endswith((".xlsx", ".xls")):
            raise ValidationError("El archivo debe ser un Excel (.xlsx o .xls)")
        return file
