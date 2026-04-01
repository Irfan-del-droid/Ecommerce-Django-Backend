from django.db import models
import uuid

class Subscriber(models.Model):
    class Source(models.TextChoices):
        WEBSITE = 'website', 'Website'
        CHECKOUT = 'checkout', 'Checkout'
        POPUP = 'popup', 'Popup'
        FOOTER = 'footer', 'Footer'
        OTHER = 'other', 'Other'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.WEBSITE)
    
    preferences = models.JSONField(default=dict) # {newArrivals, sales, news}
    
    unsubscribe_token = models.CharField(max_length=100, unique=True, blank=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    unsubscribe_reason = models.TextField(blank=True, null=True)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    last_email_sent = models.DateTimeField(blank=True, null=True)
    emails_sent = models.IntegerField(default=0)
    emails_opened = models.IntegerField(default=0)
    emails_clicked = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            self.unsubscribe_token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
