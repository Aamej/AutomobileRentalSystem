# Generated by Django 3.0.7 on 2021-05-30 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0009_remove_bookings_chargetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
