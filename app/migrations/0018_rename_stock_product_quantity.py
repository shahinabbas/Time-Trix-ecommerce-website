# Generated by Django 4.2.3 on 2023-07-31 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock',
            new_name='quantity',
        ),
    ]
