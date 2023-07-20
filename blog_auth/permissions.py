from rest_framework.permissions import BasePermission


class IsOwnerOrSuperuser(BasePermission):
    """
    Custom permission class to allow only the owner or superuser to modify a specific object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
