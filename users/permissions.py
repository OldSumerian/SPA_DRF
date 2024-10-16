from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSelfProfile(permissions.BasePermission):
    message = "Это не ваш профиль"

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk
