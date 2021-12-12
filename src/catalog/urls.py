from django.urls import path, include
from rest_framework import routers
from catalog.views import CategoryViewSet, CollectionViewSet, NFTViewSet, MyNFTsViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'collection', CollectionViewSet)
router.register(r'nft', NFTViewSet)
router.register(r'my-nfts', MyNFTsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




