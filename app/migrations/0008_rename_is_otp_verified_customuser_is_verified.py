# Generated by Django 4.2.3 on 2023-07-25 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_is_phone_verified_customuser_is_otp_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_otp_verified',
            new_name='is_verified',
        ),
    ]
