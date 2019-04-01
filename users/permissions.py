from rest_framework import permissions
from users.enums import RoleType

# permission level 0, for admins only
class IsDOEOrHigher(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == RoleType.admin or \
                request.user.is_superuser:
            return True