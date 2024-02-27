# Generated by Django 5.0.2 on 2024-02-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0012_alter_productcolor_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'تصویر محصول', 'verbose_name_plural': 'تصویر های محصول'},
        ),
        migrations.AddField(
            model_name='product',
            name='visited_ip',
            field=models.GenericIPAddressField(null=True, verbose_name='بازدید'),
        ),
    ]
