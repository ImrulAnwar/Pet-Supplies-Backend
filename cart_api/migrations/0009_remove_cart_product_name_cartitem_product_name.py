# Generated by Django 4.2.3 on 2023-08-06 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_api', '0008_cart_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product_name',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_name',
            field=models.CharField(default='no product name', max_length=1000),
        ),
    ]