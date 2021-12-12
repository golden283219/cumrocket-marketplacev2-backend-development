# Generated by Django 3.2.2 on 2021-07-13 16:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kyc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sender', models.CharField(max_length=250)),
                ('message', models.TextField()),
                ('tip', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kyc.kycmodel')),
            ],
        ),
    ]