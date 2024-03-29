# Generated by Django 5.0.2 on 2024-03-09 12:21

import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IndexApp', '0002_siteinfo_main_picture_siteinfo_side_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteinfo',
            name='main_picture',
        ),
        migrations.RemoveField(
            model_name='siteinfo',
            name='side_picture',
        ),
        migrations.CreateModel(
            name='MainPictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[831, 353], upload_to='main_picture', verbose_name='تصویر اصلی')),
                ('site_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_pictures', to='IndexApp.siteinfo')),
            ],
        ),
        migrations.CreateModel(
            name='SidePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[261, 106], upload_to='side_picture', verbose_name='تصویر کناری')),
                ('site_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side_pictures', to='IndexApp.siteinfo')),
            ],
        ),
    ]
