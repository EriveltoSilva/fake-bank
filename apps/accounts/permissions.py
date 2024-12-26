""" custom users permissions module"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Returns True if the user is the owner of the specified object"""

    def has_permission(self, request, view):
        # Permitir apenas usuários autenticados
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permitir que o proprietário do objeto (usuário) edite os próprios dados
        return obj == request.user


class IsAdmin(permissions.BasePermission):
    """return true if user is a admin"""

    def has_permission(self, request, view):
        # Permitir apenas usuários autenticados e administradores façam alterações
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsOwnerOrAdmin(permissions.BasePermission):
    """Returns True if the user is the owner or an admin of the specified object"""

    def has_permission(self, request, view):
        # Permitir apenas usuários autenticados
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permitir se o usuário é o proprietário ou um administrador
        return obj == request.user or request.user.is_superuser
