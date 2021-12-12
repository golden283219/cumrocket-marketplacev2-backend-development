from django.urls import path, include
from rest_framework import routers
from kyc.views import KYCModelViewSet, KYCModelSearchViewSet, ValidUsernameApiView

router = routers.DefaultRouter()
router.register(r'kyc-models', KYCModelViewSet)
router.register(r'models', KYCModelSearchViewSet)

urlpatterns = [
    path('validate-username/', ValidUsernameApiView.as_view()),
    path('', include(router.urls)),
]




