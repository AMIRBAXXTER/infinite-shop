# Generated by Django 5.0.2 on 2024-03-13 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CartApp', '0006_alter_cartmodel_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartmodel',
            old_name='total_price',
            new_name='final_price',
        ),
    ]
