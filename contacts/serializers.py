from rest_framework import serializers
from .models import ContactMessage, ContactResponse

class ContactResponseSerializer(serializers.ModelSerializer):
    responder_name = serializers.CharField(source='responder.full_name', read_only=True)
    
    class Meta:
        model = ContactResponse
        fields = ('id', 'responder_name', 'message', 'created_at')

class ContactMessageSerializer(serializers.ModelSerializer):
    responses = ContactResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = (
            'id', 'name', 'email', 'subject', 'message', 'status', 
            'priority', 'assignedTo', 'responses', 'isRead', 
            'readAt', 'resolvedAt', 'created_at'
        )
        read_only_fields = ('id', 'isRead', 'readAt', 'resolvedAt', 'created_at')

    # Mapping Mongoose names
    assignedTo = serializers.IntegerField(source='assigned_to_id', allow_null=True, required=False)
    isRead = serializers.BooleanField(source='is_read', default=False)
    readAt = serializers.DateTimeField(source='read_at', allow_null=True, required=False)
    resolvedAt = serializers.DateTimeField(source='resolved_at', allow_null=True, required=False)
