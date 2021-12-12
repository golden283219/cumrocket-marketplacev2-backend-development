# Generated by Django 3.2.2 on 2021-08-03 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_fill_search_vectors'),
    ]

    operations = [
        migrations.AddField(
            model_name='nft',
            name='minted',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='nft',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]