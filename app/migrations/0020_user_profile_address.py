# Generated by Django 4.2.3 on 2023-07-31 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_user_profile_postal_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='address',
            field=models.CharField(default=1, max_length=180, verbose_name='address'),
            preserve_default=False,
        ),
    ]
