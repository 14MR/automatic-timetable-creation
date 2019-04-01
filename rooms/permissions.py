from rest_framework import permissions
from users.enums import RoleType

# permission level 0 or 1, building administrators
class IsBuildingAdminOrHigher(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # only GET, HEAD and OPTIONS requests, whoever the user is
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == RoleType.admin or request.user.role == RoleType.b_admin