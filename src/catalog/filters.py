from django_filters import rest_framework as filters
from .models import NFT

class NFTFilter(filters.FilterSet):
    categories = filters.CharFilter(
        field_name='categories__name',
        lookup_expr='iexact',
    )

    model_name = filters.CharFilter(
        field_name='kyc_model__name',
        lookup_expr='icontains',
    )

    model_username = filters.CharFilter(
        field_name='kyc_model__username',
        lookup_expr='icontains',
    )

    model_id = filters.CharFilter(
        field_name='kyc_model__pk',
        lookup_expr='exact',
    )

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )



    class Meta:
        model = NFT
        fields = ('name', 'categories', 'model_name', 'model_username', 'model_id')
