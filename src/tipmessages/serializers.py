from rest_framework import serializers
from .models import TipMessage

class TipMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipMessage
        fields = '__all__'
