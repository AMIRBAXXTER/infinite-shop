# Generated by Django 5.0.2 on 2024-03-03 20:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='address',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='UserApp.city', verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='address',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال/غیرفعال'),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='UserApp.province', verbose_name='استان'),
        ),
    ]