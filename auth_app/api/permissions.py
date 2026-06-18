from rest_framework.permissions import BasePermission

class HasRefreshCookie(BasePermission):
    """
    Custom permission that checks whether a refresh token cookie is present in the request.
    """

    # Error message returned when the permission check fails
    message = "Refresh token cookie not provided"

    def has_permission(self, request, view):
        # Check if the 'refresh_token' cookie exists and is not empty
        return bool(request.COOKIES.get("refresh_token"))
        