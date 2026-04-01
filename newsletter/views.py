from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Subscriber
from .serializers import SubscriberSerializer, SubscriptionStatsSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-created_at')
    serializer_class = SubscriberSerializer

    def get_permissions(self):
        if self.action in ['subscribe', 'unsubscribe']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        email = request.data.get('email', '').lower()
        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={
                'source': request.data.get('source', 'website'),
                'preferences': request.data.get('preferences', {'newArrivals': True, 'sales': True, 'news': True}),
                'ip_address': self.request.META.get('REMOTE_ADDR'),
                'user_agent': self.request.META.get('HTTP_USER_AGENT')
            }
        )

        if not created and subscriber.is_active:
            return Response({'detail': 'Already subscribed!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()
            
        return Response({
            'status': 'success',
            'message': 'Subscribed to the newsletter!',
            'subscriber': self.get_serializer(subscriber).data
        })

    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
        email = request.data.get('email', '').lower()
        token = request.data.get('token')
        
        try:
            subscriber = Subscriber.objects.get(email=email, unsubscribe_token=token)
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.unsubscribe_reason = request.data.get('reason', 'user-request')
            subscriber.save()
            
            return Response({'status': 'success', 'message': 'Successfully unsubscribed.'})
        except Subscriber.DoesNotExist:
            return Response({'detail': 'Invalid email or token.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        total = Subscriber.objects.count()
        active = Subscriber.objects.filter(is_active=True).count()
        unsubscribed = total - active
        
        stats = {
            'total': total,
            'active': active,
            'unsubscribed': unsubscribed,
            'unsubscribeRate': (unsubscribed / total * 100) if total > 0 else 0
        }
        
        return Response({'status': 'success', 'stats': stats})
