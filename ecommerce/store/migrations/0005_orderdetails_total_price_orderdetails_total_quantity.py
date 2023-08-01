# Generated by Django 4.1.3 on 2023-07-31 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_orderdetails_order_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='total_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='total_quantity',
            field=models.IntegerField(default=0),
        ),
    ]