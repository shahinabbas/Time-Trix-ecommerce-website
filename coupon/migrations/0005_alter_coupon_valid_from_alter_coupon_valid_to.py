# Generated by Django 4.2.4 on 2023-08-25 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0004_rename_min_amount_coupon_minimum_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(),
        ),
    ]
