from rest_framework import viewsets
from .models import TipMessage
from .serializers import TipMessageSerializer


class TipMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows create new KYC models
    """
    queryset = TipMessage.objects.all()
    serializer_class = TipMessageSerializer
