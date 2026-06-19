from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.api.permissions import HasRefreshCookie
from auth_app.api.serializers import CustomTokenObtainPairSerializer, PasswordResetSerializer, RegistrationSerializer
from django.contrib.auth.models import User
from utils.email import send_email_user
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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
            # Generate email verification token
            token = default_token_generator.make_token(user)

            # Encode user ID for use in URL
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            data = {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": str(token)
            }

            # Send activation email with activation link
            send_email_user(
                subject="Confirm your email",
                template_name="emails/confirm.html",
                context={"user": user, "url": f"http://127.0.0.1:8000/api/activate/{uidb64}/{token}/"},
                to_email=user.email
            )
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccountView(APIView):
    """
    API endpoint to activate a user account via email link.

    - Validates uidb64 and token from activation link
    - Activates the user account if valid
    """
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            # Decode user ID from base64
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            print("Decoded UID:", uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid or expired activation link"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user.is_active:
            return Response(
                {"message": "Account already activated"},
                status=status.HTTP_200_OK
            )

        # Validate activation token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Activate user account
        user.is_active = True
        user.save()

        return Response(
            {"message": "Account successfully activated"},
            status=status.HTTP_200_OK
        )
class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle user login and return JWT tokens in HttpOnly cookies.
    - Accepts POST request with: email, password
    - Returns user info and sets access and refresh tokens in cookies on successful login
    """
    permission_classes = [AllowAny]

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
                "username": user.email
            }
        })

        # Store access token in HttpOnly cookie
        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        # Store refresh token in HttpOnly cookie
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
    Logs out the user by deleting authentication cookies.
    """
    # Ensures the user is authenticated and a refresh token cookie is present
    permission_classes = [IsAuthenticated, HasRefreshCookie]
    
    def post(self, request):
        # Get refresh token from cookies
        refresh_token = request.COOKIES.get("refresh_token")

        # If a refresh token exists, blacklist it so it can no longer be used
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except:
                pass

        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, 
                            status=status.HTTP_200_OK)

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

        response = Response({"detail": "Token refreshed", "access": "new_access_token"})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response
    
class PasswortResetEmailView(APIView):
    """
    API endpoint to initiate password reset by sending a reset email.
    - Accepts POST request with: email
    - Sends password reset email with tokenized link if user exists
    """
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            # Encode user id to uidb64
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # Generate password reset token
            token = default_token_generator.make_token(user)
            # Send email
            send_email_user(
                subject="Reset your password",
                template_name="emails/password_reset.html",
                context={"url": f"http://127.0.0.1:8000/api/password_confirm/{uidb64}/{token}/"}, 
                to_email=user.email
            )
        except User.DoesNotExist:
            # do nothing to prevent user enumeration
            pass 

        return Response(
            {"detail": "An email has been sent to reset your password."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(APIView):
    """API endpoint to confirm password reset using a token."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )