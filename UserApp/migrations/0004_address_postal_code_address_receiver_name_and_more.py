# Generated by Django 5.0.2 on 2024-02-29 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0003_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='کد پستی'),
        ),
        migrations.AddField(
            model_name='address',
            name='receiver_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='تحویل گیرنده'),
        ),
        migrations.AddField(
            model_name='user',
            name='national_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='شماره ملی'),
        ),
    ]
