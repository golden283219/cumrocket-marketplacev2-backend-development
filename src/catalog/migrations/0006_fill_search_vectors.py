from django.db import migrations, transaction

def copy_thumbnails(apps, schema_editor):
    NFT = apps.get_model('catalog', 'NFT')
    nfts = NFT.objects.all()
    for nft in nfts:
        nft.save()

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_nft_search_vector'),
    ]

    operations = [
        migrations.RunPython(copy_thumbnails),
    ]