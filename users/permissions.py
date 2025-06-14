from rest_framework.permissions import BasePermission, SAFE_METHODS

# permission class to revoke delete to normal user--
class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_superuser

        return True
