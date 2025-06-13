from rest_framework.permissions import BasePermission

class isNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print(f'user authentication satus--{request.user.is_authenticated}')
        return not request.user or request.user.is_authenticated