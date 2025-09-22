"""
Comando para crear usuarios de la API
====================================

Este comando crea usuarios específicos para la API REST con los grupos
correspondientes y configuración inicial.

Uso:
    python manage.py create_api_user --username usuario1 --group CRUD_Users
    python manage.py create_api_user --username usuario2 --group ReadOnly_Users --email usuario2@example.com
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Crea usuarios para la API REST con grupos específicos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Nombre de usuario',
        )
        parser.add_argument(
            '--group',
            type=str,
            choices=['CRUD_Users', 'ReadOnly_Users', 'Admin_Users'],
            required=True,
            help='Grupo al que pertenecerá el usuario',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email del usuario',
        )
        parser.add_argument(
            '--first-name',
            type=str,
            help='Nombre del usuario',
        )
        parser.add_argument(
            '--last-name',
            type=str,
            help='Apellido del usuario',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Contraseña del usuario (si no se proporciona, se genera automáticamente)',
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='No solicitar confirmación interactiva',
        )

    def handle(self, *args, **options):
        username = options['username']
        group_name = options['group']
        email = options.get('email', '')
        first_name = options.get('first_name', '')
        last_name = options.get('last_name', '')
        password = options.get('password')
        no_input = options['no_input']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            raise CommandError(f'El usuario "{username}" ya existe.')

        # Verificar que el grupo existe
        try:
            group = Group.objects.get(name=group_name)
        except ObjectDoesNotExist:
            raise CommandError(f'El grupo "{group_name}" no existe. Ejecuta primero: python manage.py setup_user_groups')

        # Generar contraseña si no se proporciona
        if not password:
            import secrets
            import string
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(12))

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_staff=(group_name == 'Admin_Users'),  # Solo Admin_Users pueden acceder al admin
        )

        # Asignar al grupo
        user.groups.add(group)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Usuario "{username}" creado exitosamente')
        )
        self.stdout.write(f'   - Grupo: {group_name}')
        self.stdout.write(f'   - Email: {email or "No especificado"}')
        self.stdout.write(f'   - Contraseña: {password}')
        self.stdout.write(f'   - Acceso a Admin: {"Sí" if user.is_staff else "No"}')

        if not no_input:
            self.stdout.write('\n🔧 Información adicional:')
            self.stdout.write(f'   - Para obtener token JWT: POST /api/auth/token/')
            self.stdout.write(f'   - Usar token: Authorization: Bearer <token>')
            self.stdout.write(f'   - Endpoints disponibles: /api/tournaments/, /api/teams/, etc.')

            if group_name == 'ReadOnly_Users':
                self.stdout.write(f'   - ⚠️  Este usuario solo puede LEER datos (no puede crear/editar/eliminar)')
            elif group_name == 'CRUD_Users':
                self.stdout.write(f'   - ✅ Este usuario puede hacer CRUD completo de la aplicación')
            elif group_name == 'Admin_Users':
                self.stdout.write(f'   - 🔑 Este usuario puede hacer CRUD completo + acceder a Django Admin')

        self.stdout.write('\n🎉 Usuario listo para usar en la API!')
