from django.urls import path, include
from rest_framework import routers
from .views import TipMessageViewSet

router = routers.DefaultRouter()
router.register(r'tip-message', TipMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




