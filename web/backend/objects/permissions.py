from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Write operations allowed only for the creator (or staff).
    Approved objects become read-only even for the owner, so fixes go through
    the moderation flow."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        owner = getattr(obj, 'created_by_id', None)
        return owner is not None and owner == request.user.id
