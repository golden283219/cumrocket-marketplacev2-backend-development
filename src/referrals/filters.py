from django_filters import rest_framework as filters
from .models import ReferralPayment

class ReferralPaymentFilter(filters.FilterSet):
    collection = filters.CharFilter(
        field_name='collection__name',
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


    class Meta:
        model = ReferralPayment
        fields = ('collection', 'model_name', 'model_username', 'model_id', 'from_address', 'to_address')
