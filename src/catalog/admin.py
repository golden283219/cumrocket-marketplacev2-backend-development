from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models
from .models import Category, Collection, NFT, PurchasedNFT
# from reversion.admin import VersionAdmin


class AdminImageWidget(AdminFileWidget):
    """Admin widget for showing clickable thumbnail of Image file fields"""

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, 'url', None):
            html = format_html('<a href="{0}" target="_blank"><img src="{0}" alt="{1}" width="150" height="150" style="object-fit: contain;"/></a>', value.url, str(value)) + html
        return html


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name',)
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


class NFTInline(admin.TabularInline):
    model = NFT
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

    def has_add_permission(self, request, *kwargs):
        return False


class CollectionAdmin(admin.ModelAdmin):

    list_display = ('name', 'kyc_model', 'created_at', 'modified_at')
    list_filter = ('kyc_model', 'created_at', 'modified_at')
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    inlines = [
        NFTInline,
    ]



class NFTAdmin(admin.ModelAdmin):

    list_display = ('name', 'collection', 'uri')
    list_filter = ('collection', 'created_at', 'categories__name')


class PurchasedNFTAdmin(admin.ModelAdmin):

    list_display = ('nft', 'token_id', 'buyer')
    list_filter = ('nft__collection', 'buyer',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(NFT, NFTAdmin)
admin.site.register(PurchasedNFT, PurchasedNFTAdmin)