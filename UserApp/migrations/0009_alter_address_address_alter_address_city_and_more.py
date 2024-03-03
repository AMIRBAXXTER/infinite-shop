# Generated by Django 5.0.2 on 2024-03-03 20:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0008_address_created_at_address_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(default='', max_length=200, verbose_name='آدرس'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(default='g', on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='UserApp.city', verbose_name='شهر'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(default='g', max_length=10, verbose_name='کد پستی'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='UserApp.province', verbose_name='استان'),
        ),
        migrations.AlterField(
            model_name='address',
            name='receiver_name',
            field=models.CharField(max_length=200, verbose_name='تحویل گیرنده'),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
