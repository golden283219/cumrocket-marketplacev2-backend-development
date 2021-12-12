from django.urls import path, include
from rest_framework import routers
from .views import AdViewSet

router = routers.DefaultRouter()
router.register(r'ad', AdViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




