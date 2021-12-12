from rest_framework import viewsets, mixins, status, permissions, authentication, filters
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings
from .models import Category, Collection, NFT, PurchasedNFT
from .serializers import CategorySerializer, CollectionSerializer, NFTSerializer, NFTReadOnlySerializer
from .filters import NFTFilter

import requests
import json

VIDEO = ('m1v', 'mpeg', 'mov', 'qt', 'mpa', 'mpg', 'mpe', 'avi', 'movie', 'mp4')

AUDIO = ('ra', 'aif', 'aiff', 'aifc', 'wav', 'au', 'snd', 'mp3', 'mp2')

IMAGE = ('ras', 'xwd', 'bmp', 'jpe', 'jpg', 'jpeg', 'xpm', 'ief', 'pbm', 'tif', 'gif', 'ppm', 'xbm', 'tiff', 'rgb', 'pgm', 'png', 'pnm')


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    API endpoint that allows create new Collections
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    API endpoint that allows create new Collections
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows create new Collections
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class NFTViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows create new Collections
    """
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer
    filter_class = NFTFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['search_vector']

    def get_queryset(self):
        queryset = super(NFTViewSet, self).get_queryset()
        queryset = queryset.filter(nft_id__isnull=False)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        # TODO: Add permission to only get your profile, not others.
        instance = self.get_object()
        serializer = NFTReadOnlySerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NFTReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NFTReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            file = request.FILES.get('media')
            headers = {"Authorization": "Bearer {}".format(settings.NFT_STORAGE)}
            url = 'https://api.nft.storage/upload'
            res = requests.post(url, files={'file': file}, headers=headers)

            extension = str(file).split('.')[-1]
            if extension and extension.lower() in IMAGE:
                data['media_type'] = 'image'
            elif extension and extension.lower() in VIDEO:
                data['media_type'] = 'video'
            if extension and extension.lower() in AUDIO:
                data['media_type'] = 'audio'

            nft = json.loads(res.content)

            cid = nft['value']['cid']
            uri = 'https://ipfs.io/ipfs/{}/{}'.format(cid, file)

            data['uri'] = uri
            data['thumbnail'] = request.FILES.get('media')  # TODO: Create a compressed thumbnail from image or video

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)



class MyNFTsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = NFT.objects.all()
    serializer_class = NFTSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['search_vector']

    def get_queryset(self):
        queryset = super(MyNFTsViewSet, self).get_queryset()
        buyer = self.request.GET.get('buyer', '')
        queryset = queryset.filter(nft_id__isnull=False, purchasednft__buyer__iexact=buyer)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NFTReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NFTReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)