from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer
from .services import GoogleOAuthService

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'token': str(refresh.access_token),
            'refreshToken': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class GoogleAuthView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        access_token = request.data.get('accessToken')
        
        if not access_token:
            return Response({'detail': 'Google token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        google_data = GoogleOAuthService.verify_google_token(access_token)
        user = GoogleOAuthService.get_or_create_user(google_data)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'token': str(refresh.access_token),
            'refreshToken': str(refresh),
            'user': UserSerializer(user).data
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
        
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({
            'status': 'success',
            'user': serializer.data
        })

class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request):
        user = request.user
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        
        if not user.check_password(current_password):
            return Response({'detail': 'Current password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
            
        user.set_password(new_password)
        user.save()
        return Response({'status': 'success', 'message': 'Password updated'})
