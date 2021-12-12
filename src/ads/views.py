from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.http import JsonResponse, HttpResponse
from .models import Ad
from .serializers import AdSerializer
from datetime import datetime
import random


class AdViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    API endpoint that allows create new Collections
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filterset_fields = ('slot',)

    # def get_queryset(self):
    #     now = datetime.now()
    #     queryset = self.queryset.filter(expires_at__gt=now)
    #     return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ad = random.choice(queryset)
        ad.renders += 1
        ad.save()
        return JsonResponse(AdSerializer(instance=ad).data)

    @action(detail=True, methods=['post'])
    def clicked(self, request, pk=None):
        ad = self.get_object()  # retrieve an object by pk provided
        ad.clicks += 1
        ad.save()
        return HttpResponse(status=status.HTTP_200_OK)