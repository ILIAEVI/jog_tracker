from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class NotAuthenticated(BasePermission):

    def has_permission(self, request, view):

        return not request.user or not request.user.is_authenticated
