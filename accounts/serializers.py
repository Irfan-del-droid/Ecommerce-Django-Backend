from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstName', 'lastName', 'email', 'phone', 'role', 'avatar', 'isEmailVerified', 'is_active', 'date_joined')
        read_only_fields = ('id', 'isEmailVerified', 'date_joined')
        
    # Map Django field names to match Express API output
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    isEmailVerified = serializers.BooleanField(source='is_email_verified')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # Use email as username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data.get('phone', '')
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user).data
        data['user'] = serializer
        data['status'] = 'success'
        return data
