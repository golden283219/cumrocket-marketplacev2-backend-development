from django.db import models
from kyc.models import KYCModel
from catalog.models import Collection

import uuid

class ReferralPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, blank=True, null=True)
    from_address = models.CharField(max_length=250)
    to_address = models.CharField(max_length=250)
    amount = models.FloatField()
    token_address = models.CharField(max_length=250)

    txhash = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
