from rest_framework import viewsets, mixins, status, permissions, views
from rest_framework.response import Response
from .serializers import KYCModelSerializer, KYCModelSearchSerializer
from kyc.models import KYCModel
from django.http import HttpResponse


class KYCModelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
    API endpoint that allows create new KYC models
    """
    queryset = KYCModel.objects.all()
    serializer_class = KYCModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ('id', 'username', 'wallet', 'email')

    def create(self, request, **kwargs):
        obj = super(KYCModelViewSet, self).create(request)
        # kyc_model = obj.data['id']
        # nfts = request.FILES.getlist('nfts')
        # for nft in nfts:
        #     NFTImage.objects.create(kyc_model_id=kyc_model, image=nft)
        return HttpResponse(status=status.HTTP_201_CREATED)

    # def get(self, request, pk):
    #     # TODO: Add permission to only get your profile, not others.
    #     pass
    #
    # def list(self, request, **kwargs):
    #     pass


class KYCModelSearchViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
    API endpoint that allows retrieve models
    """
    queryset = KYCModel.objects.all()
    serializer_class = KYCModelSearchSerializer
    permission_classes = []
    filterset_fields = ('id', 'username',)


class ValidUsernameApiView(views.APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')

        valid = not KYCModel.objects.filter(username__iexact=username).exists()

        response = {
            'valid': valid
        }

        return Response(response)
