# Generated by Django 3.0.7 on 2021-05-31 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0013_journeystage_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
