# Generated by Django 3.0.7 on 2021-05-30 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0005_remove_customers_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
