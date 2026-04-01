import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class GoogleOAuthService:
    @staticmethod
    def verify_google_token(access_token):
        try:
            google_response = requests.get(
                f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
            )
            
            if not google_response.ok:
                raise AuthenticationFailed('Failed to verify Google token')
                
            return google_response.json()
        except Exception as e:
            raise AuthenticationFailed(f'Google verification failed: {str(e)}')

    @staticmethod
    def get_or_create_user(google_user_data):
        email = google_user_data.get('email').lower()
        
        try:
            user = User.objects.get(email=email)
            # Update Google ID if not set
            if not user.google_id:
                user.google_id = google_user_data.get('sub')
                user.is_email_verified = True
                if google_user_data.get('picture') and not user.avatar:
                    user.avatar = google_user_data.get('picture')
                user.save()
        except User.DoesNotExist:
            # Create new user
            import random
            import string
            
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=random_password,
                first_name=google_user_data.get('given_name', 'User'),
                last_name=google_user_data.get('family_name', ''),
                google_id=google_user_data.get('sub'),
                is_email_verified=True,
                avatar=google_user_data.get('picture')
            )
            
        return user
