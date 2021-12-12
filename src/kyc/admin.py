from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models
from .models import KYCModel, Wallet
# from reversion.admin import VersionAdmin


class AdminImageWidget(AdminFileWidget):
    """Admin widget for showing clickable thumbnail of Image file fields"""

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, 'url', None):
            html = format_html('<a href="{0}" target="_blank"><img src="{0}" alt="{1}" width="150" height="150" style="object-fit: contain;"/></a>', value.url, str(value)) + html
        return html


# class NFTImageInline(admin.TabularInline):
#     model = NFTImage
#     formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
#
#     def has_add_permission(self, request, *kwargs):
#         return False


class KYCModelAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'performer_name', 'birth_date', 'status', 'tos_accepted', 'consent_promotional_use', 'joined_at')
    list_filter = ('birth_date', 'status', 'tos_accepted', 'consent_promotional_use', 'joined_at')
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    # inlines = [
    #     NFTImageInline,
    # ]



class WalletAdmin(admin.ModelAdmin):

    list_display = ('address', 'user',)


#
# class NFTImageAdmin(admin.ModelAdmin):
#
#     list_display = ('kyc_model', 'image',)
#     formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
#
#


admin.site.register(KYCModel, KYCModelAdmin)
admin.site.register(Wallet, WalletAdmin)
# admin.site.register(NFTImage, NFTImageAdmin)