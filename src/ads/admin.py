from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models
from .models import Ad

class AdminImageWidget(AdminFileWidget):
    """Admin widget for showing clickable thumbnail of Image file fields"""

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, 'url', None):
            html = format_html('<a href="{0}" target="_blank"><img src="{0}" alt="{1}" width="150" height="150" style="object-fit: contain;"/></a>', value.url, str(value)) + html
        return html


class AdAdmin(admin.ModelAdmin):

    list_display = ('slot', 'created_at', 'expires_at')
    list_filter = ('slot', 'created_at', 'expires_at')
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


admin.site.register(Ad, AdAdmin)