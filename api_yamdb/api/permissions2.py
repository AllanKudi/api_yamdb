from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method not in permissions.SAFE_METHODS
                and (obj.author == request.user 
                     or request.user.is_moderator 
                     or request.user.is_admin)
                or request.method in permissions.SAFE_METHODS)
    

class AdminOrReadOnly(permissions.BasePermission):

    message = 'Создание и изменение контента привилегия админов!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method not in permissions.SAFE_METHODS
                and (request.user.is_moderator 
                     or request.user.is_admin)
                or request.method in permissions.SAFE_METHODS)