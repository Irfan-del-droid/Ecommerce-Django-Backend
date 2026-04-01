from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyTokenObtainPairView, RegisterView, GoogleAuthView, 
    UserProfileView, ChangePasswordView
)

urlpatterns = [
    path('signup', RegisterView.as_view(), name='register'),
    path('login', MyTokenObtainPairView.as_view(), name='login'),
    path('google', GoogleAuthView.as_view(), name='google-auth'),
    path('refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('me', UserProfileView.as_view(), name='profile-me'),
    path('password', ChangePasswordView.as_view(), name='change-password'),
]
