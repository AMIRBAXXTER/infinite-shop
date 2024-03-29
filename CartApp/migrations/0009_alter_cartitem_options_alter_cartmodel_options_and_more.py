# Generated by Django 5.0.2 on 2024-03-17 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CartApp', '0008_alter_cartmodel_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'آیتم سفارش', 'verbose_name_plural': 'آیتم های سفارش'},
        ),
        migrations.AlterModelOptions(
            name='cartmodel',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات'},
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='authority',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='شماره تراکنش'),
        ),
    ]
