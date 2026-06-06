from django.urls import path
from .views import CookieTokenRefreshView, LogoutView, RegistrationView, CookieTokenObtainPairView

# ------------------------------
# Endpoints Authentication:
# ------------------------------

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    # path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]