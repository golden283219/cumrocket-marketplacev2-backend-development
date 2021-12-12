from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('catalog/', include('catalog.urls')),
    path('kyc/', include('kyc.urls')),
    path('ads/', include('ads.urls')),
    path('news/', include('news.urls')),
    path('bsc/', include('blockchain.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]




