from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
import datetime
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

def validate_over_18(value):
    today = datetime.date.today()
    years = today.year - value.year
    if years < 18:
        raise ValidationError(
            'Requires to be older than 18, you put %(value)s',
            params={'value': value},
        )

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


class Wallet(models.Model):
    address = models.CharField(max_length=256, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)

class KYCModel(models.Model):

    NEW = 'NEW'
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'

    KYC_STATUS = (
        (NEW, 'NEW'),
        (PENDING, 'PENDING'),
        (VERIFIED, 'VERIFIED'),
        (REJECTED, 'REJECTED'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name = models.CharField(max_length=250, db_index=True)
    performer_name = models.CharField(max_length=250)
    username = models.SlugField(max_length=110, unique=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, unique=True)

    status = models.CharField(max_length=20, choices=KYC_STATUS, default=NEW)

    birth_date = models.DateField(validators=[validate_over_18])
    id_card_front = models.ImageField(upload_to=PathAndRename('images/kyc/id_card_front'))
    id_card_back = models.ImageField(upload_to=PathAndRename('images/kyc/id_card_back'))
    id_card_selfie = models.ImageField(upload_to=PathAndRename('images/kyc/id_card_selfie'))
    profile_picture = models.ImageField(upload_to=PathAndRename('images/profile'), blank=True, null=True)
    cover_picture = models.ImageField(upload_to=PathAndRename('images/profile/cover'), blank=True, null=True)

    biography = models.TextField(blank=True, null=True)

    tos_accepted = models.BooleanField(default=False)
    consent_promotional_use = models.BooleanField(default=False)

    # Social networks
    twitter = models.URLField(blank=True, null=True)
    # facebook = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    # tiktok = models.URLField(blank=True, null=True)
    # youtube = models.URLField(blank=True, null=True)
    email = models.EmailField()

    joined_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} ({1})'.format(self.full_name, self.pk)


@receiver(pre_save, sender=KYCModel)
def my_callback(sender, instance, *args, **kwargs):
    if instance._state.adding:
        instance.status = KYCModel.PENDING

#
# class NFTImage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     image = models.ImageField(upload_to='images/nft')
#     kyc_model = models.ForeignKey(KYCModel, on_delete=models.CASCADE)
