from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

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
    password = serializers.CharField(write_only=True, validators=[validate_password])
    firstName = serializers.CharField(source='first_name', required=True)
    lastName = serializers.CharField(source='last_name', required=True)

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'email', 'phone', 'password')

    def create(self, validated_data):
        email = validated_data['email'].strip().lower() if isinstance(validated_data.get('email'), str) else validated_data['email']
        validated_data['email'] = email
        user = User.objects.create_user(
            username=email,  # Use email as username
            email=email,
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data.get('phone', '')
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        uf = User.USERNAME_FIELD
        if uf in attrs and isinstance(attrs[uf], str):
            raw = attrs[uf].strip().lower()
            attrs = {**attrs, uf: raw}
            # Case-insensitive match so DB emails stored with different casing still log in
            found = User.objects.filter(**{f'{uf}__iexact': raw}).first()
            if found:
                attrs = {**attrs, uf: getattr(found, uf)}
        data = super().validate(attrs)
        serializer = UserSerializer(self.user).data
        data['user'] = serializer
        data['status'] = 'success'
        # Match RegisterView / client: `token` + `refreshToken`, not JWT-default `access` / `refresh`
        data['token'] = data.pop('access')
        data['refreshToken'] = data.pop('refresh')
        return data
