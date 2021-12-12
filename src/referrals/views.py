from rest_framework import viewsets, mixins, status, permissions, authentication
from .models import ReferralPayment
from .serializers import ReferralPaymentSerializer


class ReferralPaymentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    API endpoint that allows retrieve the Referral payments
    """
    queryset = ReferralPayment.objects.all()
    serializer_class = ReferralPaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

