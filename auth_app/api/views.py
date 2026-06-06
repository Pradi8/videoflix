from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.api.serializers import CustomTokenObtainPairSerializer, RegistrationSerializer
from utils.email import send_email_user

class RegistrationView(APIView):
    """
    API endpoint for user registration.
    - Allows any user (no authentication required)
    - Accepts POST request with: fullname, email, password, repeated_password
    - Returns token and user info on successful registration
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": str(CustomTokenObtainPairSerializer.get_token(user).access_token)
            }
            send_email_user(
                subject="Confirm your email",
                template_name="emails/confirm.html",
                context={"user": user},
                to_email=user.email
            )
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle user login and return JWT tokens in HttpOnly cookies.
    - Accepts POST request with: username, password
    - Returns user info and sets access and refresh tokens in cookies on successful login
    """

    serializer_class = CustomTokenObtainPairSerializer
   
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
     
        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]

        response = Response({
            "detail": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    
        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        
        return response
    
class LogoutView(APIView):
    """ 
    Deletes access and refresh tokens from cookies
    """
    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom view tohandle token refresh using the refresh token from HttpOnly cookies.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"error": "Refresh token not provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {"error": "Invalid refresh token"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        access_token = serializer.validated_data.get("access")

        response = Response({"detail": "Token refreshed"})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response