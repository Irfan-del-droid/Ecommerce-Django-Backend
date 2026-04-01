from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import ContactMessage, ContactResponse
from .serializers import ContactMessageSerializer, ContactResponseSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_authenticators(self):
        if self.action == 'create':
            return []
        return super().get_authenticators()

    def perform_create(self, serializer):
        serializer.save(
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.read_at = timezone.now()
            instance.save()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='respond')
    def respond(self, request, pk=None):
        contact = self.get_object()
        message = request.data.get('message')
        
        if not message:
            return Response({'detail': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        ContactResponse.objects.create(
            contact_message=contact,
            responder=request.user,
            message=message
        )
        
        # Auto-update status
        if contact.status == ContactMessage.Status.PENDING:
            contact.status = ContactMessage.Status.IN_PROGRESS
        contact.save()
        
        return Response({'status': 'success', 'message': 'Response sent to the warrior!'})

    @action(detail=True, methods=['post'], url_path='resolve')
    def resolve(self, request, pk=None):
        contact = self.get_object()
        contact.status = ContactMessage.Status.RESOLVED
        contact.resolved_at = timezone.now()
        contact.save()
        return Response({'status': 'success', 'message': 'Quest resolved!'})

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        total = ContactMessage.objects.count()
        pending = ContactMessage.objects.filter(status=ContactMessage.Status.PENDING).count()
        in_progress = ContactMessage.objects.filter(status=ContactMessage.Status.IN_PROGRESS).count()
        resolved = ContactMessage.objects.filter(status=ContactMessage.Status.RESOLVED).count()
        
        stats = {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'resolved': resolved,
            'resolutionRate': (resolved / total * 100) if total > 0 else 0
        }
        
        return Response({'status': 'success', 'stats': stats})
