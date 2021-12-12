from django.db import migrations, transaction

def copy_thumbnails(apps, schema_editor):
    NFT = apps.get_model('catalog', 'NFT')
    nfts = NFT.objects.all()
    for nft in nfts:
        nft.thumbnail = nft.media
        nft.media_type = 'image'
        nft.save()

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210723_1222'),
    ]

    operations = [
        migrations.RunPython(copy_thumbnails),
    ]