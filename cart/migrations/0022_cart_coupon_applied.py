# Generated by Django 4.2.4 on 2023-08-08 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
        ('cart', '0021_rename_order_orderitem_order_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_applied',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coupon.coupon'),
        ),
    ]
