from django.db import models
import uuid

class Ad(models.Model):

    SLOT_SIZES = (
        ('1X1', '1X1'),
        ('2X1', '2X1'),
        ('3X1', '3X1'),
        ('4X1', '4X1'),
        ('1X2', '1X2'),
        ('1X3', '1X3'),
        ('1X4', '1X4'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    slot = models.CharField(max_length=10, choices=SLOT_SIZES, help_text='Columns x Rows. 2X1 means two columns width and 1 row height.')
    image = models.ImageField(upload_to='images/ads')

    clicks = models.IntegerField(default=0)
    renders = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return '{0} ({1})'.format(self.slot, self.pk)
