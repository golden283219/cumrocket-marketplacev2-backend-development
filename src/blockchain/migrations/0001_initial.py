# Generated by Django 3.2.2 on 2021-07-14 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LastPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('last_price', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
