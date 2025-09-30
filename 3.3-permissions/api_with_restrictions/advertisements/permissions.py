from rest_framework import permissions


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """
    Предоставление прав на изменение и удаление только автору объявления
    """
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить изменение и удаление только автору объявления или администратору
        return obj.creator == request.user or request.user.is_staff