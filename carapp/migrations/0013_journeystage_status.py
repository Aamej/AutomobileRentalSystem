# Generated by Django 3.0.7 on 2021-05-31 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0012_payment_nameoncard'),
    ]

    operations = [
        migrations.AddField(
            model_name='journeystage',
            name='status',
            field=models.CharField(default='Open', max_length=20),
        ),
    ]
