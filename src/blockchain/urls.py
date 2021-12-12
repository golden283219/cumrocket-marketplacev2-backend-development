from django.urls import path, include
from rest_framework import routers
from blockchain.views import CumRocketPriceAPIView, sync

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("price/", CumRocketPriceAPIView.as_view(), name="price"),
    path("sync/", sync, name="sync"),
]




