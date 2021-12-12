from django.contrib import admin
from django.db import models
from .models import TipMessage


class TipMessageAdmin(admin.ModelAdmin):

    list_display = ('sender', 'to', 'tip', 'created_at')
    list_filter = ('sender', 'to', 'tip', 'created_at')


admin.site.register(TipMessage, TipMessageAdmin)