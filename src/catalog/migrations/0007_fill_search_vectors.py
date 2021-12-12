from django.db import migrations, transaction

def copy_thumbnails(apps, schema_editor):
    NFT = apps.get_model('catalog', 'NFT')
    nfts = NFT.objects.all()
    for instance in nfts:
        collection_name = instance.collection.name if instance.collection else ''
        instance.search_vector = ' '.join([str(s) for s in [instance.kyc_model.full_name,
                                        instance.kyc_model.username, instance.kyc_model.performer_name,
                                        instance.name, instance.description, collection_name]])
        instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_fill_search_vectors'),
    ]

    operations = [
        migrations.RunPython(copy_thumbnails),
    ]