from rest_framework import serializers
from catalog.models import Category, Tag, Collection, NFT
from kyc.serializers import KYCModelReadOnlySerializer

from urllib.parse import urlparse, urljoin


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class NFTSerializer(serializers.ModelSerializer):

    minted = serializers.SerializerMethodField(read_only=True)

    def get_minted(self, obj):
        return obj.minted

    class Meta:
        model = NFT
        fields = '__all__'

class NFTReadOnlySerializer(serializers.ModelSerializer):

    kyc_model = KYCModelReadOnlySerializer()
    collection = CollectionSerializer()

    minted = serializers.SerializerMethodField(read_only=True)

    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    def get_thumbnail_url(self, obj):
        if obj.media_type == NFT.AUDIO:
            return ""
        ext = ".png" if obj.media_type == NFT.IMAGE else ".gif"
        url = obj.media.url
        return urljoin(url, urlparse(url).path.replace("/nfts/", "/thumbnails/")).rsplit(".", 1)[0] + ext

    def get_minted(self, obj):
        return obj.minted

    class Meta:
        model = NFT
        fields = '__all__'
