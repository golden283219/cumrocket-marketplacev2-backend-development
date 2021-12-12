from django.contrib import admin
from django.db import models
from .models import ReferralPayment



class ReferralPaymentAdmin(admin.ModelAdmin):

    list_display = ('collection', 'from_address', 'to_address', 'amount', 'token_address')
    list_filter = ('collection', 'amount', 'token_address')

admin.site.register(ReferralPayment, ReferralPaymentAdmin)