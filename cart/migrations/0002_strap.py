# Generated by Django 4.2.3 on 2023-07-30 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_cartitem_cart_remove_cartitem_product_and_more'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strap', models.CharField(max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
    ]
