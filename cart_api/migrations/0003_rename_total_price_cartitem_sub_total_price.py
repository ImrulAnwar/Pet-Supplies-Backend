# Generated by Django 4.2.3 on 2023-07-29 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart_api', '0002_cart_item_count_cart_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='total_price',
            new_name='sub_total_price',
        ),
    ]
