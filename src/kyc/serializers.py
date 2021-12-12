from rest_framework import serializers
from kyc.models import KYCModel

class KYCModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCModel
        fields = '__all__'

class KYCModelReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCModel
        fields = ('id', 'full_name', 'performer_name', 'profile_picture', 'username', 'status', 'cover_picture',
                  'biography', 'twitter', 'website', 'instagram', 'wallet')

class KYCModelSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCModel
        fields = ('id', 'full_name', 'performer_name', 'profile_picture', 'username', 'status', 'cover_picture',
                  'biography', 'twitter', 'website', 'instagram',)

# class ProfileKYCModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KYCModel
#         fields = ('id', )


# class NFTImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NFTImage
#         fields = '__all__'
