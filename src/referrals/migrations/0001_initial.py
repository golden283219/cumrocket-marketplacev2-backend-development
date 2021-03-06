# Generated by Django 3.2.2 on 2021-07-14 19:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralPayment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('from_address', models.CharField(max_length=250)),
                ('to_address', models.CharField(max_length=250)),
                ('amount', models.FloatField()),
                ('token_address', models.CharField(max_length=250)),
                ('txhash', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.collection')),
            ],
        ),
    ]
