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
    """Must stay anonymous + no JWT parsing so stale Bearer headers cannot break login."""
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        """Browser GET shows how to call signup; registration itself is POST-only."""
        return Response({
            'detail': 'Send POST with application/json to register.',
            'method': 'POST',
            'url': request.build_absolute_uri(),
            'body': {
                'first_name': 'string (required)',
                'last_name': 'string (required)',
                'email': 'string (required)',
                'password': 'string (required)',
                'phone': 'string (optional, 10 digits)',
            },
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = serializer.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'token': str(refresh.access_token),
            'refreshToken': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class GoogleAuthView(APIView):
    authentication_classes = ()
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
