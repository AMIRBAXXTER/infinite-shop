# Generated by Django 5.0.2 on 2024-03-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0018_alter_category_url_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(default=150, verbose_name='وزن به گرم'),
            preserve_default=False,
        ),
    ]