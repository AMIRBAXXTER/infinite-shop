# Generated by Django 5.0.2 on 2024-03-13 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0009_alter_address_address_alter_address_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, verbose_name='نام انگلیسی'),
        ),
        migrations.AddField(
            model_name='province',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, verbose_name='نام انگلیسی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images', verbose_name='تصویر پروفایل'),
        ),
        migrations.AlterModelTable(
            name='city',
            table='cities',
        ),
        migrations.AlterModelTable(
            name='province',
            table='provinces',
        ),
    ]
