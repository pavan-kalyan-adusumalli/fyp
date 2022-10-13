# Generated by Django 4.0.4 on 2022-05-02 05:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_shop_maplink'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='orderstatus',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='orders',
            name='ordertotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shop',
            name='date_created',
            field=models.CharField(default=datetime.date(2022, 5, 2), max_length=15),
        ),
    ]
