from rest_framework import permissions
from users.enums import RoleType

# permission level 0 or 1, building administrators
class IsBuildingAdminOrHigher(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # only GET, HEAD and OPTIONS requests, whoever the user is
        if request.method in permissions.SAFE_METHODS or \
                request.user.role == RoleType.admin or request.user.role == RoleType.b_admin or \
                request.user.is_superuser:
            return True