from rest_framework import permissions

class IsMember(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated


class IsOwner(permissions.DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or user.is_superuser