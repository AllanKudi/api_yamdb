from rest_framework import permissions

message = 'Данный запрос недоступен для вас.'


class IsAdminUser(permissions.BasePermission):
    """Доступ только для пользователей с ролью администратора."""

    print(message)

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAuthorOrModerAdminOrReadOnly(permissions.BasePermission):
    """Даёт доступ неадмину/немодеру/неавтору только к GET/OPTIONS/HEAD."""

    print(message)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Даёт доступ неадмину только к GET/OPTIONS/HEAD."""

    print(message)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)
