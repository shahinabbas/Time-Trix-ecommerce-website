# Generated by Django 4.2.3 on 2023-07-31 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_remove_cartitem_strap_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quantity',
            new_name='Quantity',
        ),
    ]
