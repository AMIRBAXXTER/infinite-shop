# Generated by Django 5.0.2 on 2024-03-01 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_alter_user_national_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='card_number',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='شماره کارت'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل'),
        ),
    ]
