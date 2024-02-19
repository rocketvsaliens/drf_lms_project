from rest_framework import permissions

from lms.models import Course


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email
