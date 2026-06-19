from django.urls import path
from .views import ActivateAccountView, CookieTokenRefreshView, LogoutView, PasswordResetConfirmView, PasswortResetEmailView, RegistrationView, CookieTokenObtainPairView

# ------------------------------
# Endpoints Authentication:
# ------------------------------

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswortResetEmailView.as_view(), name='password_reset'),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_confirm'),
]