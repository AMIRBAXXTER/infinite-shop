# Generated by Django 5.0.2 on 2024-02-24 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0009_productcomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_description',
            field=models.TextField(default='test', verbose_name='توضیحات اصلی'),
            preserve_default=False,
        ),
    ]
