from django.urls import path, include
from rest_framework import routers
from .views import ReferralPaymentViewSet

router = routers.DefaultRouter()
router.register(r'referral-payment', ReferralPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




