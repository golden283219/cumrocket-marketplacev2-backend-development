# Generated by Django 3.2.2 on 2021-08-13 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_purchasednft_nft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nft',
            name='minted',
        ),
    ]
