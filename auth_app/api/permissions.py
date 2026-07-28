from rest_framework.permissions import BasePermission

class HasRefreshCookie(BasePermission):
    """
    Custom permission that checks whether a refresh token cookie is present in the request.
    """
    message = "Refresh token cookie not provided"

    def has_permission(self, request, view):
        return bool(request.COOKIES.get("refresh_token"))
        