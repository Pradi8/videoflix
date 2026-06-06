from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the access token
    from an HttpOnly cookie instead of the Authorization header.
    """

    def authenticate(self, request):
        # Get the access token from the browser cookie
        token = request.COOKIES.get("access_token")

        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except InvalidToken:
            return None