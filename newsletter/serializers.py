from rest_framework import serializers
from .models import Subscriber

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('id', 'email', 'isActive', 'source', 'preferences', 'created_at')
        read_only_fields = ('id', 'created_at')

    # Mapping Mongoose names
    isActive = serializers.BooleanField(source='is_active', default=True)

class SubscriptionStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    active = serializers.IntegerField()
    unsubscribed = serializers.IntegerField()
    unsubscribeRate = serializers.DecimalField(max_digits=5, decimal_places=2)
