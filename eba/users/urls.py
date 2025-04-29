from django.urls import path
from .views import UserRegistraion,UserLogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegistraion.as_view(), name='register'),
    path('auth/login/', UserLogin.as_view(), name='register'),
]