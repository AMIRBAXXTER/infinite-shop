# Generated by Django 5.0.2 on 2024-02-28 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0016_product_sale_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url_title',
            field=models.SlugField(default='must-set', verbose_name='عنوان در url'),
            preserve_default=False,
        ),
    ]
