# Generated by Django 4.2.4 on 2023-08-15 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_rename_product_id_wishlist_product_and_more'),
        ('coupon', '0004_rename_min_amount_coupon_minimum_amount'),
        ('cart', '0029_remove_cart_razor_pay_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_charge',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='coupon_applied',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coupon.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.user_profile'),
        ),
    ]
