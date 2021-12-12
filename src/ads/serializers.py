from rest_framework import serializers
from ads.models import Ad

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('slot', 'image', 'pk')

