from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишн. Только безопасный метод.
    Небезопасный - доступ для автора/модератора/админа.
    """
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        """Проверка безопасного метода или авторизации."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Проверка НЕбезопасного метода и прав автора\админа\модератора.
        Или проверка безопасного метода.
        """
        return (request.method not in permissions.SAFE_METHODS
                and (obj.author == request.user 
                     or request.user.is_moderator 
                     or request.user.is_admin)
                or request.method in permissions.SAFE_METHODS)
    

class AdminOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишн. Только безопасный метод.
    Небезопасный - доступ для модератора/админа.
    Разница с первым в том, что тут не предусмотрен автор.
    """
    message = 'Создание и изменение контента - привилегия админов!'

    def has_permission(self, request, view):
        """Проверка безопасного метода или авторизации."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Проверка НЕбезопасного метода и прав админа\модератора.
        Или проверка безопасного метода.
        """
        return (request.method not in permissions.SAFE_METHODS
                and (request.user.is_moderator 
                     or request.user.is_admin)
                or request.method in permissions.SAFE_METHODS)