# Generated by Django 4.0.4 on 2022-05-10 06:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderstatus',
            field=models.CharField(default='Order Placed', help_text='Help customer to track orderby entering tracking status.', max_length=100),
        ),
        migrations.AlterField(
            model_name='shop',
            name='date_created',
            field=models.CharField(default=datetime.date(2022, 5, 10), max_length=15),
        ),
    ]
