# Generated by Django 4.2.4 on 2023-08-08 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0020_order_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='order',
            new_name='order_no',
        ),
    ]
