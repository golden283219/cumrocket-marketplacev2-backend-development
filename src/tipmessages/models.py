from django.db import models
from kyc.models import KYCModel
import uuid

class TipMessage(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    to = models.ForeignKey(KYCModel, on_delete=models.CASCADE)

    sender = models.CharField(max_length=250)
    message = models.TextField()
    tip = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} for {1} ({2})'.format(self.sender, self.tip, self.pk)
