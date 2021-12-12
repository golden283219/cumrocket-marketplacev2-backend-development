from django.urls import path, include
from .views import LoginAPIView, LoginVerifyApiView, Web3LoginAPIView

urlpatterns = [
    path('magiclink/login/', LoginAPIView.as_view()),
    path('magiclink/login/verify/', LoginVerifyApiView.as_view()),
    path('web3/login/', Web3LoginAPIView.as_view()),
    path('', include('magiclink.urls', namespace='magiclink')),
]




