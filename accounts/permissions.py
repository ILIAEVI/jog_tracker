from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Check if the user has the 'admin' role for other methods
        return request.user.is_authenticated and request.user.role == 'admin'
