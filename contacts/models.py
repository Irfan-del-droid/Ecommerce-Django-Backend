from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactMessage(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in-progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=5000)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_contacts')
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Set priority based on subject
            if self.subject in ['order', 'return']:
                self.priority = self.Priority.HIGH
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class ContactResponse(models.Model):
    contact_message = models.ForeignKey(ContactMessage, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
