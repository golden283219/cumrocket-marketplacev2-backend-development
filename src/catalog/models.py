from django.db import models
from kyc.models import KYCModel
from django.db.models.signals import pre_save
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver

import os
import uuid

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

class Category(models.Model):

    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class Tag(models.Model):

    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class Collection(models.Model):
    """
    1. Frontend send NewCollection (modelName is username that is name of collection).
    2. .then() -> get txHash and send the POST to backend.
    3. Backend gets the modelContractAddress (if txHash is successful).
    4. Frontend pings to getTransactionReciept(txhash),
      4.1 If successful, don't do nothing.
      4.2 If fails, send DELETE to backend.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=250, db_index=True, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    txhash = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    kyc_model = models.ForeignKey(KYCModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class NFT(models.Model):

    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'

    MEDIA_TYPE = (
        (IMAGE, 'image'),
        (VIDEO, 'video'),
        (AUDIO, 'audio'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kyc_model = models.ForeignKey(KYCModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to=PathAndRename('nfts'))
    media_type = models.CharField(max_length=50, blank=True, null=True)
    thumbnail = models.FileField(upload_to=PathAndRename('thumbnails'), blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)  # IPFS url
    address = models.CharField(max_length=255, blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, blank=True, null=True)
    categories = models.ManyToManyField(Category)

    price = models.FloatField(blank=True, null=True)
    token_address = models.CharField(max_length=255, blank=True, null=True)
    mint_cap = models.IntegerField(blank=True, null=True)
    # minted = models.IntegerField(default=0, blank=True, null=True)
    nft_id = models.CharField(max_length=255, blank=True, null=True)
    txhash = models.URLField(blank=True, null=True)

    search_vector = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def minted(self):
        return len(self.purchasednft_set.all())


class PurchasedNFT(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, blank=True, null=True)
    token_id = models.CharField(max_length=255, blank=True, null=True)
    buyer = models.CharField(max_length=255, blank=True, null=True)
    txhash = models.URLField(blank=True, null=True)


@receiver(pre_save, sender=NFT)
def my_callback(sender, instance, *args, **kwargs):
    instance.thumbnail = instance.media  #TODO: instance.thumbnail must be converted to an @attribute
    collection_name = instance.collection.name if instance.collection else ''
    instance.search_vector = ' '.join([str(s) for s in [instance.kyc_model.full_name, instance.kyc_model.username,
                                      instance.kyc_model.performer_name, instance.name, instance.description,
                                       collection_name]])
