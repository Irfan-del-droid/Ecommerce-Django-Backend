from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    # Field mapping from original Mongoose model
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'

    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^[0-9]{10}$', message="Please enter a valid 10-digit phone number")
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    
    google_id = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    
    last_login = models.DateTimeField(blank=True, null=True)
    login_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(blank=True, null=True)
    
    # Django uses username by default, but we'll use email for login login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
