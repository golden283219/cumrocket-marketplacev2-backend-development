from django.db import models

class LastPrice(models.Model):

    data = models.JSONField()
    last_price = models.DateTimeField(auto_now=True)