from rest_framework import permissions


class IsProjectOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True
        return obj.owner == request.user.id