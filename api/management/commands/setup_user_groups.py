"""
Comando para configurar grupos de usuarios y permisos
====================================================

Este comando crea los grupos de usuarios necesarios para el sistema de permisos
de la API REST y asigna los permisos correspondientes.

Grupos creados:
- CRUD_Users: Acceso completo al CRUD de la aplicación
- ReadOnly_Users: Solo lectura de todos los modelos
- Admin_Users: Acceso completo (incluye Django Admin)

Uso:
    python manage.py setup_user_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Configura grupos de usuarios y permisos para la API REST'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina y recrea todos los grupos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🔄 Eliminando grupos existentes...')
            Group.objects.filter(name__in=[
                'CRUD_Users', 'ReadOnly_Users', 'Admin_Users'
            ]).delete()

        self.stdout.write('🚀 Configurando grupos de usuarios...')

        # Obtener todos los content types de los modelos de la aplicación
        content_types = ContentType.objects.filter(
            app_label__in=['tournaments', 'teams', 'matches', 'events']
        )

        # Obtener permisos de lectura
        read_permissions = Permission.objects.filter(
            content_type__in=content_types,
            codename__startswith='view_'
        )

        # Obtener permisos de escritura (add, change, delete)
        write_permissions = Permission.objects.filter(
            content_type__in=content_types,
            codename__in=['add_tournament', 'change_tournament', 'delete_tournament',
                         'add_tournamentcategory', 'change_tournamentcategory', 'delete_tournamentcategory',
                         'add_phase', 'change_phase', 'delete_phase',
                         'add_round', 'change_round', 'delete_round',
                         'add_team', 'change_team', 'delete_team',
                         'add_player', 'change_player', 'delete_player',
                         'add_match', 'change_match', 'delete_match',
                         'add_matchteam', 'change_matchteam', 'delete_matchteam',
                         'add_matchevent', 'change_matchevent', 'delete_matchevent']
        )

        # Crear grupo CRUD_Users (acceso completo)
        crud_group, created = Group.objects.get_or_create(name='CRUD_Users')
        if created:
            self.stdout.write('✅ Grupo CRUD_Users creado')
        else:
            self.stdout.write('ℹ️  Grupo CRUD_Users ya existe')
        
        # Asignar todos los permisos al grupo CRUD_Users
        all_permissions = read_permissions | write_permissions
        crud_group.permissions.set(all_permissions)
        self.stdout.write(f'✅ {all_permissions.count()} permisos asignados a CRUD_Users')

        # Crear grupo ReadOnly_Users (solo lectura)
        readonly_group, created = Group.objects.get_or_create(name='ReadOnly_Users')
        if created:
            self.stdout.write('✅ Grupo ReadOnly_Users creado')
        else:
            self.stdout.write('ℹ️  Grupo ReadOnly_Users ya existe')
        
        # Asignar solo permisos de lectura
        readonly_group.permissions.set(read_permissions)
        self.stdout.write(f'✅ {read_permissions.count()} permisos de lectura asignados a ReadOnly_Users')

        # Crear grupo Admin_Users (acceso completo + admin)
        admin_group, created = Group.objects.get_or_create(name='Admin_Users')
        if created:
            self.stdout.write('✅ Grupo Admin_Users creado')
        else:
            self.stdout.write('ℹ️  Grupo Admin_Users ya existe')
        
        # Asignar todos los permisos + permisos de admin
        admin_permissions = all_permissions | Permission.objects.filter(
            content_type__app_label='auth'
        )
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(f'✅ {admin_permissions.count()} permisos asignados a Admin_Users')

        self.stdout.write('\n🎉 Configuración de grupos completada!')
        self.stdout.write('\n📋 Grupos disponibles:')
        self.stdout.write('  - CRUD_Users: Acceso completo al CRUD de la aplicación')
        self.stdout.write('  - ReadOnly_Users: Solo lectura de todos los modelos')
        self.stdout.write('  - Admin_Users: Acceso completo (incluye Django Admin)')
        
        self.stdout.write('\n🔧 Para asignar usuarios a grupos:')
        self.stdout.write('  - Desde Django Admin: /admin/auth/group/')
        self.stdout.write('  - Desde código: user.groups.add(Group.objects.get(name="CRUD_Users"))')
        
        self.stdout.write('\n🚀 Para probar la API:')
        self.stdout.write('  - Obtener token: POST /api/auth/token/')
        self.stdout.write('  - Usar token: Authorization: Bearer <token>')
        self.stdout.write('  - Endpoints: /api/tournaments/, /api/teams/, etc.')
