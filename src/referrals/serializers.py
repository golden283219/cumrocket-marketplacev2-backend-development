from rest_framework import serializers
from .models import ReferralPayment


class ReferralPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralPayment
        fields = '__all__'
