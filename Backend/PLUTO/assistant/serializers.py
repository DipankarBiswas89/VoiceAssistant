from rest_framework import serializers
from .models import Interaction

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['user_input', 'ai_response', 'created_at']