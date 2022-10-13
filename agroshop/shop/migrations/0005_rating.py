# Generated by Django 4.0.4 on 2022-05-02 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_orders_delivary_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('date', models.CharField(max_length=20)),
                ('rated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userratings', to='shop.asusers')),
                ('rated_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productratings', to='shop.product')),
            ],
        ),
    ]
