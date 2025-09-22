"""
Sistema de Permisos Personalizado para Don Bosco Cup API
======================================================

Este módulo define permisos personalizados para controlar el acceso a la API REST.
Permite crear usuarios con acceso limitado al CRUD sin acceso a Django Admin.

Grupos de Usuarios:
- CRUD_Users: Acceso completo a CRUD de la aplicación
- ReadOnly_Users: Solo lectura de todos los modelos
- Admin_Users: Acceso completo (incluye Django Admin)

Uso:
1. Crear grupos con permisos específicos
2. Asignar usuarios a grupos
3. Los permisos se aplican automáticamente en la API
"""

from rest_framework import permissions


class IsCRUDUser(permissions.BasePermission):
    """
    Permiso personalizado que permite acceso completo al CRUD
    para usuarios del grupo 'CRUD_Users' o superusuarios.
    """
    
    def has_permission(self, request, view):
        # Superusuarios siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar si el usuario pertenece al grupo CRUD_Users
        return request.user.groups.filter(name='CRUD_Users').exists()


class IsReadOnlyUser(permissions.BasePermission):
    """
    Permiso personalizado que permite solo lectura
    para usuarios del grupo 'ReadOnly_Users'.
    """
    
    def has_permission(self, request, view):
        # Superusuarios siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar si el usuario pertenece al grupo ReadOnly_Users
        return request.user.groups.filter(name='ReadOnly_Users').exists()


class IsCRUDOrReadOnlyUser(permissions.BasePermission):
    """
    Permiso que permite CRUD completo a usuarios CRUD_Users
    y solo lectura a usuarios ReadOnly_Users.
    """
    
    def has_permission(self, request, view):
        # Superusuarios siempre tienen acceso completo
        if request.user.is_superuser:
            return True
            
        # Usuarios CRUD_Users tienen acceso completo
        if request.user.groups.filter(name='CRUD_Users').exists():
            return True
            
        # Usuarios ReadOnly_Users solo pueden leer
        if request.user.groups.filter(name='ReadOnly_Users').exists():
            return request.method in permissions.SAFE_METHODS
            
        return False


class IsAdminOrCRUDUser(permissions.BasePermission):
    """
    Permiso que permite acceso completo a administradores y usuarios CRUD.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_superuser or 
            request.user.is_staff or
            request.user.groups.filter(name='CRUD_Users').exists()
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite solo al propietario del objeto modificar,
    otros usuarios solo pueden leer.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura para cualquier request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Permisos de escritura solo para el propietario o superusuarios
        return (
            request.user.is_superuser or
            request.user.groups.filter(name='CRUD_Users').exists()
        )
